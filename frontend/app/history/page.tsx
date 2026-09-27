/**
 * Page Historique ("/history")
 * Regroupe Chat, Révision et QCM, avec un sélecteur pour filtrer par type.
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Loading from "@/components/Loading";
import ErrorMessage from "@/components/ErrorMessage";
import { getHistory, HistoryItem } from "@/lib/api";
import { useT } from "@/lib/i18n";
import { useLanguage } from "@/lib/preferences";

type FilterType = "all" | "chat" | "revision" | "quiz";

const TYPE_ICON: Record<string, string> = {
  chat: "💬",
  revision: "📖",
  quiz: "📝",
};

export default function HistoryPage() {
  const [filter, setFilter] = useState<FilterType>("all");
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const router = useRouter();
  const t = useT();
  const { language } = useLanguage();

  const load = useCallback((type: FilterType) => {
    setLoading(true);
    setError(false);
    getHistory(type === "all" ? undefined : type)
      .then((data) => setItems(data.conversations))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load(filter);
  }, [filter, load]);

  function openItem(item: HistoryItem) {
    if (item.type === "chat" && item.id) {
      router.push(`/chat?conversation=${item.id}`);
    } else if (item.type === "revision") {
      router.push(`/revision?module=${item.module || ""}&course=${item.course || ""}`);
    } else if (item.type === "quiz") {
      router.push(`/quiz?module=${item.module || ""}&course=${item.course || ""}`);
    }
  }

  const FILTERS: { value: FilterType; label: string }[] = [
    { value: "all", label: t("history_filter_all") },
    { value: "chat", label: t("history_filter_chat") },
    { value: "revision", label: t("history_filter_revision") },
    { value: "quiz", label: t("history_filter_quiz") },
  ];

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">
        <h1 className="mb-4 text-xl font-bold text-epf-dark">🕘 {t("history_title")}</h1>

        <div className="mb-6 flex gap-2">
          {FILTERS.map((f) => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`rounded-xl px-4 py-2 text-sm font-medium transition ${
                filter === f.value
                  ? "bg-epf-pink text-white"
                  : "bg-white text-epf-dark shadow-sm hover:shadow-md"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>

        {loading && <Loading label={t("history_loading")} />}
        {error && <ErrorMessage message={t("history_error")} onRetry={() => load(filter)} />}
        {!loading && !error && items.length === 0 && <p className="text-epf-gray">{t("history_empty")}</p>}

        <div className="flex max-w-xl flex-col gap-2">
          {items.map((item, index) => (
            <button
              key={`${item.type}-${item.id}-${index}`}
              onClick={() => openItem(item)}
              className="flex items-center justify-between rounded-xl bg-white px-4 py-3 text-left text-sm shadow-sm transition hover:shadow-md"
            >
              <span className="font-medium text-epf-dark">
                {TYPE_ICON[item.type]} {item.title}
              </span>
              <span className="text-xs text-epf-gray">
                {new Date(item.created_at).toLocaleDateString(language === "fr" ? "fr-FR" : "en-GB")}
              </span>
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}
