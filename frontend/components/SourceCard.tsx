/**
 * Carte affichant les sources d'une réponse (cours, chapitre, page) — Responsable : Personne 3
 */

type Source = {
  course: string;
  chapter: string;
  page: number;
};

export default function SourceCard({ sources }: { sources: Source[] }) {
  return (
    <div>
      {/* TODO: afficher chaque source (📚 cours — page X) */}
    </div>
  );
}
