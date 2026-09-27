/**
 * Zone de conversation : liste des messages (question / réponse), sources,
 * like/dislike + régénération, et bouton "écouter" (texte -> audio).
 */

"use client";

import { useRef, useState } from "react";
import SourceCard from "./SourceCard";
import FeedbackButtons from "./FeedbackButtons";
import { Source, synthesizeSpeech } from "@/lib/api";
import { useT } from "@/lib/i18n";

/**
 * Détection simple de la langue d'un texte (français vs anglais), pour
 * choisir la bonne voix côté Azure Text-to-Speech.
 *
 * IMPORTANT : les regex précédentes n'avaient pas le flag "g", donc
 * `.match()` ne comptait jamais plus d'une occurrence au total (le score
 * était toujours 0 ou 1 des deux côtés) : la détection ne fonctionnait
 * quasiment jamais correctement, d'où la voix française utilisée même
 * sur une réponse en anglais. On ajoute le flag "g" + des frontières de
 * mots (\b) pour compter correctement toutes les occurrences.
 */
function detectLanguage(text: string): "fr-FR" | "en-US" {
  const frenchWords =
    /\b(le|la|les|un|une|des|est|pour|avec|dans|qui|que|vous|nous|c'est|être|donc|mais|sur|cours|comment|pourquoi|qu'est-ce)\b/gi;
  const englishWords =
    /\b(the|is|are|this|that|with|for|you|your|what|how|and|of|to|it|course|does|do|can|explain)\b/gi;
  const frenchAccents = /[éèêëàùçôâîïû]/g;

  const frenchScore = (text.match(frenchWords) || []).length + (text.match(frenchAccents) || []).length;
  const englishScore = (text.match(englishWords) || []).length;

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
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const t = useT();

  /** Coupe net la lecture en cours, si il y en a une. */
  function stopListening() {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    audioRef.current = null;
    setPlayingIndex(null);
  }

  async function handleListen(index: number, text: string) {
    // On coupe une éventuelle lecture précédente avant d'en démarrer une autre.
    stopListening();
    setPlayingIndex(index);
    try {
      const language = detectLanguage(text);
      const audioBlob = await synthesizeSpeech(text, language);
      const url = URL.createObjectURL(audioBlob);
      const audio = new Audio(url);
      audioRef.current = audio;
      audio.onended = () => {
        audioRef.current = null;
        setPlayingIndex(null);
      };
      await audio.play();
    } catch {
      alert("Impossible de lire la réponse à voix haute.");
      audioRef.current = null;
      setPlayingIndex(null);
    }
  }

  /** Simple clic = écouter, double clic = arrêter (seulement si c'est ce message qui joue). */
  function handleListenClick(index: number, text: string) {
    if (playingIndex === index) return; // déjà en lecture : le double-clic gère l'arrêt
    handleListen(index, text);
  }

  function handleListenDoubleClick(index: number) {
    if (playingIndex === index) stopListening();
  }

  if (messages.length === 0) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center text-center text-epf-gray">
        <p className="text-2xl font-semibold text-epf-dark">{t("chat_hello_generic")}</p>
        <p className="mt-1">{t("chat_intro")}</p>
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
                  onClick={() => handleListenClick(index, message.content)}
                  onDoubleClick={() => handleListenDoubleClick(index)}
                  className="text-xs text-epf-gray hover:text-epf-pink"
                  title={
                    playingIndex === index
                      ? "Double-clique pour arrêter la lecture"
                      : t("chat_listen")
                  }
                >
                  {playingIndex === index ? `🔊 ${t("chat_listening")}` : `🔊 ${t("chat_listen")}`}
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
