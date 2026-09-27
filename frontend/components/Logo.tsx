/**
 * Logo "EPFind" : le rond dégradé rouge/violet du logo EPF (recréé en SVG,
 * pas une image copiée), suivi de "ind" pour former "EPFind" en un seul mot,
 * comme demandé (epf + ind = EPFind).
 * Cliquable : renvoie vers l'accueil (ou vers `href`).
 */

import Link from "next/link";

export default function Logo({
  size = 40,
  href = "/",
  dark = false,
}: {
  size?: number;
  href?: string;
  dark?: boolean;
}) {
  return (
    <Link href={href} className="flex items-center gap-1.5" aria-label="Accueil EPFind">
      <svg width={size} height={size} viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="epfind-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3B1E5E" />
            <stop offset="100%" stopColor="#C6122E" />
          </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="50" fill="url(#epfind-gradient)" />
        {/* "epf" stylisé avec la boucle caractéristique du logo de l'école */}
        <text
          x="50"
          y="62"
          textAnchor="middle"
          fontFamily="Georgia, serif"
          fontSize="34"
          fontStyle="italic"
          fill="white"
        >
          epf
        </text>
        <path
          d="M68 38 a12 12 0 1 1 -8 20"
          stroke="white"
          strokeWidth="4"
          fill="none"
          strokeLinecap="round"
        />
      </svg>
      <span
        className={`text-xl font-extrabold tracking-tight ${
          dark ? "text-white" : "text-epf-dark"
        }`}
      >
        EPF<span className="text-epf-pink">ind</span>
      </span>
    </Link>
  );
}
