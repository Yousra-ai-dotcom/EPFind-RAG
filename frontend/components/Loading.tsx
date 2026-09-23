/**
 * Indicateur de chargement réutilisable (spinner + texte).
 */

"use client";

import { useT } from "@/lib/i18n";

export default function Loading({ label }: { label?: string }) {
  const t = useT();
  return (
    <div
      className="flex items-center gap-3 text-sm text-epf-gray"
      role="status"
      aria-live="polite"
    >
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-epf-pink-light border-t-epf-pink" />
      {label ?? t("common_loading")}
    </div>
  );
}