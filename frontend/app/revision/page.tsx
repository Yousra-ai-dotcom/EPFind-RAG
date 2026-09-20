/**
 * Page Révision ("/revision") 
 *
 * - Sélecteur de cours
 * - Choix du type de révision (résumé rapide / détaillé / points clés / fiche / explication)
 * - Bouton "Générer ma révision" -> POST /summarize
 * - Affichage du résultat formaté
 */

"use client";

import { useState } from "react";
import { generateSummary } from "@/lib/api";

const SUMMARY_TYPES = [
  { value: "resume_rapide", label: "Résumé rapide" },
  { value: "resume_detaille", label: "Résumé détaillé" },
  { value: "points_cles", label: "Points clés" },
  { value: "fiche_de_revision", label: "Fiche de révision" },
  { value: "explication_pedagogique", label: "Explication pédagogique" },
];

export default function RevisionPage() {
  const [course, setCourse] = useState("");
  const [summaryType, setSummaryType] = useState("resume_rapide");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    setLoading(true);
    try {
      const data = await generateSummary(course, summaryType);
      setResult(data.summary);
    } catch (error) {
      setResult("Une erreur est survenue, réessayez.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Choisissez votre cours</h1>

      <input
        className="border p-2 w-full mb-4"
        value={course}
        onChange={(e) => setCourse(e.target.value)}
        placeholder="Nom du cours (ex: Machine Learning)"
      />

      <h2 className="text-lg font-semibold mb-2">Comment voulez-vous réviser ?</h2>

      <div className="flex flex-col gap-2 mb-4">
        {SUMMARY_TYPES.map((type) => (
          <label key={type.value} className="flex items-center gap-2">
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
        className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
        onClick={handleGenerate}
        disabled={loading || !course}
      >
        {loading ? "Génération..." : "Générer ma révision"}
      </button>

      {result && (
        <div className="mt-6 whitespace-pre-line border-t pt-4">{result}</div>
      )}
    </main>
  );
}