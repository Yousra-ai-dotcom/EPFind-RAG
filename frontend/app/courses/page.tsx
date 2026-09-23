/**
 * Page "Mes cours" ("/courses")
 * Liste les cours via GET /courses (getCourses), avec recherche et grille de cartes.
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Loading from "@/components/Loading";
import ErrorMessage from "@/components/ErrorMessage";
import { getCourses } from "@/lib/api";

export default function CoursesPage() {
  const [courses, setCourses] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    setError(false);
    getCourses()
      .then((data) => setCourses(data.courses))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  // Filtre la liste selon la recherche (sans tenir compte des majuscules)
  const filtered = courses.filter((course) =>
    course.toLowerCase().includes(search.trim().toLowerCase())
  );

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-6">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <h1 className="text-xl font-bold text-epf-dark">📚 Mes cours</h1>
          <input
            className="w-full max-w-xs rounded-xl border border-epf-pink-light bg-white px-4 py-2.5 text-sm focus:border-epf-pink focus:outline-none"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Rechercher un cours..."
            aria-label="Rechercher un cours"
          />
        </div>

        {loading && <Loading label="Chargement des cours..." />}

        {error && (
          <ErrorMessage
            message="Impossible de charger les cours. Le serveur ne répond pas."
            onRetry={load}
          />
        )}

        {!loading && !error && courses.length === 0 && (
          <p className="text-epf-gray">Aucun cours disponible pour le moment.</p>
        )}

        {!loading && !error && courses.length > 0 && filtered.length === 0 && (
          <p className="text-epf-gray">Aucun cours ne correspond à « {search} ».</p>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((course) => (
            <div
              key={course}
              className="rounded-xl2 bg-white p-5 shadow-sm transition hover:shadow-md"
            >
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-epf-pink-light text-lg">
                📘
              </div>
              <h2 className="text-sm font-semibold text-epf-dark">{course}</h2>
              <p className="mt-1 text-xs text-epf-gray">Cours indexé dans EPFind</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}