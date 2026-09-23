/**
 * Indicateur de chargement réutilisable (spinner + texte).
 */
export default function Loading({ label = "Chargement..." }: { label?: string }) {
  return (
    <div
      className="flex items-center gap-3 text-sm text-epf-gray"
      role="status"
      aria-live="polite"
    >
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-epf-pink-light border-t-epf-pink" />
      {label}
    </div>
  );
}