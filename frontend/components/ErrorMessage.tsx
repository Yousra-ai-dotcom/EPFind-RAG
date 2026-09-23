/**
 * Message d'erreur réutilisable, avec bouton "Réessayer" optionnel.
 */
type Props = {
  message?: string;
  onRetry?: () => void;
};

export default function ErrorMessage({
  message = "Une erreur est survenue.",
  onRetry,
}: Props) {
  return (
    <div
      role="alert"
      className="flex max-w-xl items-center justify-between gap-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      <span>{message}</span>
      {onRetry && (
        <button
          onClick={onRetry}
          className="rounded-lg bg-red-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-red-700"
        >
          Réessayer
        </button>
      )}
    </div>
  );
}