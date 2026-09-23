/**
 * Carte affichant les sources d'une réponse (cours, chapitre, page).
 */

import { Source } from "@/lib/api";

export default function SourceCard({ sources }: { sources: Source[] }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 rounded-xl border border-epf-pink-light bg-epf-pink-light/40 p-3">
      <p className="mb-2 text-xs font-semibold text-epf-pink-dark">📚 Sources</p>
      <ul className="flex flex-col gap-1">
        {sources.map((source, index) => (
          <li key={index} className="text-xs text-epf-gray">
            {source.course}
            {source.chapter ? ` — ${source.chapter}` : ""}
            {source.page ? ` — page ${source.page}` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}
