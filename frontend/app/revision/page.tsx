/**
 * Page Révision ("/revision")
 */

"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import ModuleCourseSelect from "@/components/ModuleCourseSelect";
import Toast from "@/components/Toast";
import { generateSummary } from "@/lib/api";
import { useT } from "@/lib/i18n";

export default function RevisionPage() {
  const [module, setModule] = useState("");
  const [course, setCourse] = useState("");
  const [summaryType, setSummaryType] = useState("resume_rapide");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);
  const t = useT();

  const SUMMARY_TYPES = [
    { value: "resume_rapide", label: t("revision_type_quick") },
    { value: "resume_detaille", label: t("revision_type_detailed") },
    { value: "points_cles", label: t("revision_type_key_points") },
    { value: "fiche_de_revision", label: t("revision_type_sheet") },
    { value: "explication_pedagogique", label: t("revision_type_pedagogic") },
  ];

  async function handleGenerate() {
    if (!course) {
      setToast({ message: t("revision_empty_course"), type: "error" });
      return;
    }

    setLoading(true);
    setResult("");
    try {
      const data = await generateSummary(course, summaryType, module || undefined);
      setResult(data.summary);
      setToast({ message: t("revision_done"), type: "success" });
    } catch (err) {
      setResult("");
      const detail = err instanceof Error ? err.message : "";
      setToast({ message: detail ? `${t("revision_error")} (${detail})` : t("revision_error"), type: "error" });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-6">
        <h1 className="mb-6 text-xl font-bold text-epf-dark">📖 {t("revision_title")}</h1>

        <div className="max-w-2xl rounded-xl2 bg-white p-6 shadow-sm">
          <label className="mb-2 block text-sm font-semibold text-epf-dark">
            {t("revision_module_course")}
          </label>
          <ModuleCourseSelect
            module={module}
            course={course}
            onModuleChange={setModule}
            onCourseChange={setCourse}
          />

          <label className="mb-2 mt-6 block text-sm font-semibold text-epf-dark">
            {t("revision_how")}
          </label>
          <div className="flex flex-col gap-2">
            {SUMMARY_TYPES.map((type) => (
              <label
                key={type.value}
                className={`flex cursor-pointer items-center gap-3 rounded-xl border px-4 py-2.5 text-sm ${
                  summaryType === type.value
                    ? "border-epf-pink bg-epf-pink-light"
                    : "border-epf-pink-light"
                }`}
              >
                <input
                  type="radio"
                  name="summaryType"
                  value={type.value}
                  checked={summaryType === type.value}
                  onChange={(e) => setSummaryType(e.target.value)}
                />
                {type.label}
              </label>
            ))}
          </div>

          <button
            className="mt-6 w-full rounded-xl bg-epf-pink py-3 text-sm font-semibold text-white transition hover:bg-epf-pink-dark disabled:opacity-60"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? t("revision_generating") : t("revision_generate")}
          </button>
        </div>

        {result && (
          <div className="mt-6 max-w-2xl whitespace-pre-line rounded-xl2 bg-white p-6 text-sm leading-relaxed text-epf-dark shadow-sm">
            {result}
          </div>
        )}
      </main>

      {toast && (
        <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />
      )}
    </div>
  );
}
