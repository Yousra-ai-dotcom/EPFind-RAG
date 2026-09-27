/**
 * Page d'accueil ("/") — non connectée. Toutes les actions redirigent
 * vers /login : seuls les étudiants EPF (compte Microsoft) peuvent
 * utiliser l'application.
 */

import Link from "next/link";
import Logo from "@/components/Logo";

const FEATURES = [
  { icon: "💬", label: "Chat", desc: "Posez vos questions et obtenez une réponse basée sur vos cours." },
  { icon: "📚", label: "Mes cours", desc: "Retrouvez tous les cours EPF indexés, classés par module." },
  { icon: "📖", label: "Révision", desc: "Générez une fiche de révision claire à partir d'un cours." },
  { icon: "📝", label: "QCM", desc: "Testez vos connaissances avec un quiz généré automatiquement." },
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#f7f6fa]">
      <header className="flex items-center justify-between border-b border-epf-pink-light bg-white px-8 py-4">
        <Logo size={40} />
        <Link
          href="/login"
          className="rounded-xl bg-epf-pink px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-epf-pink-dark"
        >
          Se connecter avec Microsoft
        </Link>
      </header>

      <section className="flex flex-col items-center gap-3 px-8 py-16 text-center">
        <h1 className="max-w-2xl text-3xl font-extrabold text-epf-dark sm:text-4xl">
          Votre assistant intelligent pour les cours EPF
        </h1>
        <p className="max-w-xl text-epf-gray">
          Bienvenue dans votre espace étudiant ! Posez vos questions, révisez et
          testez-vous, directement à partir de vos cours.
        </p>
      </section>

      <section className="mx-auto grid max-w-4xl grid-cols-1 gap-4 px-8 pb-20 sm:grid-cols-2">
        {FEATURES.map((f) => (
          <Link
            key={f.label}
            href="/login"
            className="flex items-start gap-4 rounded-xl2 bg-white p-5 text-left shadow-sm transition hover:shadow-md"
          >
            <span className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-xl bg-epf-pink-light text-xl">
              {f.icon}
            </span>
            <div>
              <h2 className="text-sm font-bold text-epf-dark">{f.label}</h2>
              <p className="mt-1 text-xs text-epf-gray">{f.desc}</p>
            </div>
          </Link>
        ))}
      </section>
    </main>
  );
}
