/**
 * Barre latérale de navigation — visible sur toutes les pages "app"
 * (chat, révision, QCM, historique).
 */

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Logo from "./Logo";

const LINKS = [
  { href: "/chat", label: "Question", icon: "💬" },
  { href: "/revision", label: "Révision", icon: "📚" },
  { href: "/quiz", label: "QCM", icon: "📝" },
  { href: "/history", label: "Historique", icon: "🕘" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 flex-col justify-between border-r border-epf-pink-light bg-white px-4 py-6">
      <div>
        <Link href="/">
          <Logo size={32} />
        </Link>

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
                    : "text-epf-dark hover:bg-epf-pink-light"
                }`}
              >
                <span>{link.icon}</span>
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="rounded-xl bg-epf-pink-light p-3 text-xs text-epf-gray">
        EPF Find — assistant intelligent pour vos cours EPF.
      </div>
    </aside>
  );
}
