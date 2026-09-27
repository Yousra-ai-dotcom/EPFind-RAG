/**
 * Carte affichant les sources d'une réponse (module, cours, document, page).
 * Chaque source est cliquable : ouvre une popup avec le détail, et un lien
 * pour ouvrir/télécharger le vrai PDF du cours (l'app ne sait pas encore
 * ouvrir directement à la bonne page, ce n'est pas possible sans un lecteur
 * PDF dédié, mais l'étudiant peut ouvrir le document et aller à la page indiquée).
 */

"use client";

import { useState } from "react";
import { Source, getCourseDownloadUrl } from "@/lib/api";
import { useT } from "@/lib/i18n";

export default function SourceCard({ sources }: { sources: Source[] }) {
  const [selected, setSelected] = useState<Source | null>(null);
  const t = useT();

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 rounded-xl border border-epf-pink-light bg-epf-pink-light/40 p-3">
      <p className="mb-2 text-xs font-semibold text-epf-pink-dark">📚 Sources</p>
      <ul className="flex flex-col gap-1">
        {sources.map((source, index) => (
          <li key={index}>
            <button
              onClick={() => setSelected(source)}
              className="text-left text-xs text-epf-pink-dark underline decoration-dotted hover:text-epf-pink"
            >
              📄 {source.document || source.course}
              {source.page ? ` — page ${source.page}` : ""}
            </button>
          </li>
        ))}
      </ul>

      {selected && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
          onClick={() => setSelected(null)}
        >
          <div
            className="w-full max-w-sm rounded-xl2 bg-white p-5 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="mb-3 text-sm font-bold text-epf-dark">Source</h3>
            <ul className="flex flex-col gap-1 text-sm text-epf-gray">
              {selected.module && <li><b>Module :</b> {selected.module}</li>}
              <li><b>Cours :</b> {selected.course}</li>
              {selected.document && <li><b>Document :</b> {selected.document}</li>}
              {selected.page && <li><b>Page :</b> {selected.page} (à chercher dans le PDF ci-dessous)</li>}
            </ul>

            <a
              href={getCourseDownloadUrl(selected.course, selected.module)}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-block rounded-lg bg-epf-pink px-4 py-1.5 text-xs font-semibold text-white hover:bg-epf-pink-dark"
            >
              📄 Ouvrir le document PDF
            </a>
            <button
              onClick={() => setSelected(null)}
              className="ml-2 mt-4 rounded-lg border border-epf-pink-light px-4 py-1.5 text-xs font-semibold text-epf-dark"
            >
              {t("common_close")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
