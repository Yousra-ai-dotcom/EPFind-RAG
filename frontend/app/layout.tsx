/**
 * Layout racine Next.js — Responsable : Personne 3
 * Englobe toutes les pages (police, styles globaux, éventuel provider d'auth).
 */
import "./globals.css";

export const metadata = {
  title: "EPF Find",
  description: "Votre assistant intelligent pour les cours EPF",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
