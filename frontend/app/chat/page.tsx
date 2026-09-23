/**
 * Page Question/Chat ("/chat")
 */

"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import CourseSelector from "@/components/CourseSelector";
import Chat, { ChatMessage } from "@/components/Chat";
import { askQuestion } from "@/lib/api";

export default function ChatPage() {
  const [course, setCourse] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;

    const userMessage: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const result = await askQuestion(question, course || undefined, conversationId);
      setConversationId(result.conversation_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.answer, sources: result.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Une erreur est survenue, réessaie." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <main className="flex flex-1 flex-col p-6">
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-epf-dark">💬 Poser une question</h1>
          <div className="w-64">
            <CourseSelector value={course} onChange={setCourse} allowAll />
          </div>
        </div>

        <Chat messages={messages} />

        <div className="mt-4 flex gap-2">
          <input
            className="flex-1 rounded-xl border border-epf-pink-light bg-white px-4 py-3 text-sm focus:border-epf-pink focus:outline-none"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Pose ta question sur tes cours EPF..."
          />
          <button
            className="rounded-xl bg-epf-pink px-6 py-3 text-sm font-semibold text-white transition hover:bg-epf-pink-dark disabled:opacity-60"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "..." : "Envoyer"}
          </button>
        </div>
      </main>
    </div>
  );
}
