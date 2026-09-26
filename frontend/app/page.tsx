/**
 * Page d'accueil ("/")
 */

import Link from "next/link";
import Logo from "@/components/Logo";

const SHORTCUTS = [
  { href: "/revision", icon: "📚", label: "Réviser" },
  { href: "/chat", icon: "💬", label: "Poser une question" },
  { href: "/quiz", icon: "📝", label: "QCM" },
  { href: "/history", icon: "🕘", label: "Historique" },
];

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 bg-gradient-to-b from-epf-pink-light to-white p-8">
      <Logo size={56} />

      <p className="max-w-md text-center text-epf-gray">
        Votre assistant intelligent pour les cours EPF : posez vos questions,
        révisez et testez-vous, directement à partir de vos cours.
      </p>

      <Link
        href="/login"
        className="rounded-xl bg-epf-pink px-8 py-3 font-semibold text-white shadow-lg shadow-epf-pink/30 transition hover:bg-epf-pink-dark"
      >
        Se connecter avec Microsoft
      </Link>

      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {SHORTCUTS.map((s) => (
          <Link
            key={s.href}
            href={s.href}
            className="flex flex-col items-center gap-2 rounded-xl2 bg-white px-6 py-4 text-sm font-medium text-epf-dark shadow-sm transition hover:shadow-md"
          >
            <span className="text-2xl">{s.icon}</span>
            {s.label}
          </Link>
        ))}
      </div>
    </main>
  );
}
