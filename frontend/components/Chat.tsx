/**
 * Zone de conversation : liste des messages (question / réponse) + sources.
 */

import SourceCard from "./SourceCard";
import { Source } from "@/lib/api";

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export default function Chat({ messages }: { messages: ChatMessage[] }) {
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
          </div>
        </div>
      ))}
    </div>
  );
}
