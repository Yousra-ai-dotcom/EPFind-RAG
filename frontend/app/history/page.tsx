/**
 * Page Historique ("/history")
 * Liste les conversations de l'utilisateur, avec états de chargement et d'erreur.
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Loading from "@/components/Loading";
import ErrorMessage from "@/components/ErrorMessage";
import { getHistory } from "@/lib/api";
import { useT } from "@/lib/i18n";
import { useLanguage } from "@/lib/preferences";

type Conversation = { id: number; title: string; created_at: string };

export default function HistoryPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const router = useRouter();
  const t = useT();
  const { language } = useLanguage();

  const load = useCallback(() => {
    setLoading(true);
    setError(false);
    getHistory()
      .then((data) => setConversations(data.conversations))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">
        <h1 className="mb-6 text-xl font-bold text-epf-dark">🕘 {t("history_title")}</h1>

        {loading && <Loading label={t("history_loading")} />}

        {error && <ErrorMessage message={t("history_error")} onRetry={load} />}

        {!loading && !error && conversations.length === 0 && (
          <p className="text-epf-gray">{t("history_empty")}</p>
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
                {new Date(c.created_at).toLocaleDateString(
                  language === "fr" ? "fr-FR" : "en-GB"
                )}
              </span>
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}