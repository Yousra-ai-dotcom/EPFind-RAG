/**
 * Page Historique ("/history")
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import { getHistory } from "@/lib/api";

type Conversation = { id: number; title: string; created_at: string };

export default function HistoryPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    getHistory()
      .then((data) => setConversations(data.conversations))
      .catch(() => setConversations([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-xl font-bold text-epf-dark">🕘 Historique</h1>

        {loading && <p className="text-epf-gray">Chargement...</p>}
        {!loading && conversations.length === 0 && (
          <p className="text-epf-gray">Aucune conversation pour le moment.</p>
        )}

        <div className="flex max-w-xl flex-col gap-2">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => router.push(`/chat?conversation=${c.id}`)}
              className="flex items-center justify-between rounded-xl bg-white px-4 py-3 text-left text-sm shadow-sm transition hover:shadow-md"
            >
              <span className="font-medium text-epf-dark">{c.title}</span>
              <span className="text-xs text-epf-gray">
                {new Date(c.created_at).toLocaleDateString("fr-FR")}
              </span>
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}
