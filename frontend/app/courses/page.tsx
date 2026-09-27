/**
 * Page "Mes cours" ("/courses")
 * On choisit d'abord un module, puis les cours de ce module s'affichent
 * en grille de cartes cliquables (ouvre le Chat avec ce cours pré-sélectionné).
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Loading from "@/components/Loading";
import ErrorMessage from "@/components/ErrorMessage";
import { getCourses } from "@/lib/api";
import { DEMO_MODE, DEMO_COURSES } from "@/lib/demo";
import { useT } from "@/lib/i18n";

export default function CoursesPage() {
  const [modules, setModules] = useState<Record<string, string[]>>({});
  const [module, setModule] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const t = useT();
  const router = useRouter();

  const load = useCallback(() => {
    setError(false);

    if (DEMO_MODE) {
      setModules({ Démo: DEMO_COURSES });
      setLoading(false);
      return;
    }

    setLoading(true);
    getCourses()
      .then((data) => setModules(data.modules || {}))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const moduleNames = Object.keys(modules);
  const coursesForModule = module ? modules[module] || [] : [];
  const filtered = coursesForModule.filter((course) =>
    course.toLowerCase().includes(search.trim().toLowerCase())
  );

  function openCourse(course: string) {
    router.push(`/chat?module=${encodeURIComponent(module)}&course=${encodeURIComponent(course)}`);
  }

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-6">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <h1 className="text-xl font-bold text-epf-dark">📚 {t("courses_title")}</h1>
        </div>

        {loading && <Loading label={t("courses_loading")} />}
        {error && <ErrorMessage message={t("courses_error")} onRetry={load} />}

        {!loading && !error && (
          <>
            <div className="mb-4 flex flex-wrap gap-2">
              {moduleNames.map((m) => (
                <button
                  key={m}
                  onClick={() => setModule(m)}
                  className={`rounded-xl px-4 py-2 text-sm font-medium transition ${
                    module === m
                      ? "bg-epf-pink text-white"
                      : "bg-white text-epf-dark shadow-sm hover:shadow-md"
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>

            {!module && <p className="text-epf-gray">{t("courses_choose_module")}</p>}

            {module && (
              <>
                <input
                  className="mb-4 w-full max-w-xs rounded-xl border border-epf-pink-light bg-white px-4 py-2.5 text-sm focus:border-epf-pink focus:outline-none"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder={t("courses_search")}
                  aria-label={t("courses_search")}
                />

                {coursesForModule.length === 0 && (
                  <p className="text-epf-gray">{t("courses_empty")}</p>
                )}

                {coursesForModule.length > 0 && filtered.length === 0 && (
                  <p className="text-epf-gray">{t("courses_no_match").replace("{search}", search)}</p>
                )}

                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
                  {filtered.map((course) => (
                    <button
                      key={course}
                      onClick={() => openCourse(course)}
                      className="rounded-xl2 bg-white p-5 text-left shadow-sm transition hover:shadow-md hover:ring-2 hover:ring-epf-pink"
                    >
                      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-epf-pink-light text-lg">
                        📘
                      </div>
                      <h2 className="text-sm font-semibold text-epf-dark">{course}</h2>
                      <p className="mt-1 text-xs text-epf-gray">{t("courses_card_sub")}</p>
                      <p className="mt-2 text-xs font-semibold text-epf-pink">{t("courses_open")} →</p>
                    </button>
                  ))}
                </div>
              </>
            )}
          </>
        )}
      </main>
    </div>
  );
}
