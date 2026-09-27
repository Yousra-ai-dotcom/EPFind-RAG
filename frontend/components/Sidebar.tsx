/**
 * Barre latérale de navigation - visible sur toutes les pages "app".
 * Thème sombre (comme l'app EPF iLearn), élément actif surligné en rouge.
 * Applique aussi le thème clair/sombre choisi et la langue (useApplyPreferences).
 * Vérifie que l'étudiant est bien connecté (sinon redirige vers /login).
 */

"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Logo from "./Logo";
import { logout, useRequireAuth } from "@/lib/auth";
import { useApplyPreferences } from "@/lib/preferences";
import { useT, TKey } from "@/lib/i18n";

const LINKS: { href: string; key: TKey; icon: string }[] = [
  { href: "/chat", key: "nav_chat", icon: "💬" },
  { href: "/courses", key: "nav_courses", icon: "📚" },
  { href: "/revision", key: "nav_revision", icon: "📖" },
  { href: "/quiz", key: "nav_quiz", icon: "📝" },
  { href: "/history", key: "nav_history", icon: "🕘" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const t = useT();
  useApplyPreferences();
  useRequireAuth(); // connexion Microsoft obligatoire pour accéder à l'app

  async function handleLogout() {
    try {
      await logout();
    } catch {
      // pas de session active : on continue quand même
    }
    router.push("/login");
  }

  return (
    <aside className="flex h-screen w-64 flex-col justify-between bg-epf-dark px-4 py-6">
      <div>
        <Logo size={32} dark />

        <nav className="mt-10 flex flex-col gap-1">
          {LINKS.map((link) => {
            const active = pathname?.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-medium transition-colors ${
                  active
                    ? "bg-epf-pink text-white"
                    : "text-white/70 hover:bg-white/10 hover:text-white"
                }`}
              >
                <span>{link.icon}</span>
                {t(link.key)}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="rounded-xl bg-white/10 p-3">
        <Link
          href="/profile"
          className={`flex items-center gap-3 rounded-lg p-1 transition hover:bg-white/10 ${
            pathname?.startsWith("/profile") ? "bg-white/10" : ""
          }`}
        >
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-epf-pink text-sm font-bold text-white">
            E
          </span>
          <span className="text-sm font-semibold text-white">{t("nav_profile")}</span>
        </Link>
        <button
          onClick={handleLogout}
          className="mt-2 w-full rounded-lg px-2 py-1.5 text-left text-xs font-medium text-white/60 transition hover:bg-white/10 hover:text-white"
        >
          ⎋ {t("nav_logout")}
        </button>
      </div>
    </aside>
  );
}
