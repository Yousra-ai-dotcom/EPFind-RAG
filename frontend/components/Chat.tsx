/**
 * Zone de conversation : liste des messages (question / réponse), sources,
 * like/dislike + régénération, et bouton "écouter" (texte -> audio).
 */

"use client";

import { useState } from "react";
import SourceCard from "./SourceCard";
import FeedbackButtons from "./FeedbackButtons";
import { Source, synthesizeSpeech } from "@/lib/api";

/**
 * Détection très simple de la langue d'un texte (français vs anglais),
 * pour choisir la bonne voix côté Azure Text-to-Speech. Pas parfait,
 * mais suffisant pour distinguer une réponse en français d'une réponse
 * en anglais.
 */
function detectLanguage(text: string): "fr-FR" | "en-US" {
  const frenchHints = /[éèêàùçôâ]| le | la | les | un | une | est | pour | avec | dans | qui | que /i;
  const englishHints = / the | is | are | this | that | with | for | you | your | what | how /i;

  const padded = ` ${text.toLowerCase()} `;
  const frenchScore = (padded.match(frenchHints) || []).length;
  const englishScore = (padded.match(englishHints) || []).length;

  return englishScore > frenchScore ? "en-US" : "fr-FR";
}

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  liked?: boolean | null;
};

type Props = {
  messages: ChatMessage[];
  onFeedback?: (messageIndex: number, liked: boolean | null) => void;
  onRegenerate?: (messageIndex: number) => void;
};

export default function Chat({ messages, onFeedback, onRegenerate }: Props) {
  const [playingIndex, setPlayingIndex] = useState<number | null>(null);

  async function handleListen(index: number, text: string) {
    setPlayingIndex(index);
    try {
      const language = detectLanguage(text);
      const audioBlob = await synthesizeSpeech(text, language);
      const url = URL.createObjectURL(audioBlob);
      const audio = new Audio(url);
      audio.onended = () => setPlayingIndex(null);
      await audio.play();
    } catch {
      alert("Impossible de lire la réponse à voix haute.");
      setPlayingIndex(null);
    }
  }

  if (messages.length === 0) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center text-center text-epf-gray">
        <p className="text-2xl font-semibold text-epf-dark">Bonjour 👋</p>
        <p className="mt-1">Que veux-tu apprendre aujourd&apos;hui ?</p>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col gap-4 overflow-y-auto px-2 py-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
              message.role === "user"
                ? "bg-epf-pink text-white"
                : "bg-white text-epf-dark shadow-sm"
            }`}
          >
            <p className="whitespace-pre-line">{message.content}</p>

            {message.role === "assistant" && message.sources && (
              <SourceCard sources={message.sources} />
            )}

            {message.role === "assistant" && (
              <div className="mt-2 flex items-center gap-3">
                <button
                  onClick={() => handleListen(index, message.content)}
                  disabled={playingIndex === index}
                  className="text-xs text-epf-gray hover:text-epf-pink"
                  title="Écouter la réponse"
                >
                  {playingIndex === index ? "🔊 Lecture..." : "🔊 Écouter"}
                </button>

                {onFeedback && onRegenerate && (
                  <FeedbackButtons
                    question={messages[index - 1]?.content || ""}
                    answer={message.content}
                    liked={message.liked}
                    onFeedback={(liked) => onFeedback(index, liked)}
                    onRegenerate={() => onRegenerate(index)}
                  />
                )}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
