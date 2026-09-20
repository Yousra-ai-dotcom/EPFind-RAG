/**
 * Page d'accueil ("/") 
 *
 * - Logo + titre "EPF Find"
 * - Bouton "Se connecter avec Microsoft" -> /login
 * - Accès rapide : Réviser / Poser une question / QCM / Historique
 */

import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-8">
      <h1 className="text-4xl font-bold">EPF Find</h1>
      <p className="text-gray-500">
        Votre assistant intelligent pour les cours EPF
      </p>

      <Link
        href="/login"
        className="rounded-lg bg-blue-600 px-6 py-3 text-white"
      >
        Se connecter avec Microsoft
      </Link>

      <div className="flex gap-4">
        <Link href="/revision">📚 Réviser</Link>
        <Link href="/chat">💬 Poser une question</Link>
        <Link href="/quiz">📝 QCM</Link>
        <Link href="/history">🕘 Historique</Link>
      </div>
    </main>
  );
}