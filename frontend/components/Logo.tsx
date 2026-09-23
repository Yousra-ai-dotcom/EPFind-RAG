/**
 * Logo "EPF Find" — inspiré des couleurs du logo EPF (rose/magenta),
 * recréé en SVG (pas une copie du logo officiel de l'école).
 */

export default function Logo({ size = 40 }: { size?: number }) {
  return (
    <div className="flex items-center gap-2">
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="20" cy="20" r="20" fill="#E6007E" />
        <path
          d="M13 27V13h13"
          stroke="white"
          strokeWidth="3.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M13 20h9"
          stroke="white"
          strokeWidth="3.2"
          strokeLinecap="round"
        />
      </svg>
      <span className="text-xl font-extrabold tracking-tight text-epf-dark">
        EPF <span className="text-epf-pink">Find</span>
      </span>
    </div>
  );
}
