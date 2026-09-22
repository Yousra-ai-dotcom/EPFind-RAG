/**
 * Page Question/Chat ("/chat") 
 *
 * TODO :
 * - Sélecteur de cours (CourseSelector)
 * - Zone de conversation (Chat)
 * - Champ de saisie de question -> POST /ask via lib/api.ts
 * - Affichage réponse + sources (SourceCard)
 */

"use client";

import { useState } from "react";
import { askQuestion } from "@/lib/api";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    setLoading(true);
    const result = await askQuestion(question);
    setAnswer(result.answer);
    setLoading(false);
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Poser une question</h1>

      <input
        className="border p-2 w-full"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Pose ta question..."
      />

      <button
        className="mt-2 rounded bg-blue-600 px-4 py-2 text-white"
        onClick={handleAsk}
        disabled={loading}
      >
        {loading ? "Recherche..." : "Envoyer"}
      </button>

      {answer && <p className="mt-4">{answer}</p>}
    </main>
  );
}