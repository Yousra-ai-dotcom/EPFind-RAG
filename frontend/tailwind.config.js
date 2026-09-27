/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: ["class", '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        // Couleurs alignées sur l'app EPF iLearn (dégradé rouge/violet du logo),
        // à la place du rose utilisé précédemment. Les noms de classes ne
        // changent pas (epf-pink, epf-pink-dark, epf-pink-light) pour ne pas
        // avoir à toucher tous les composants qui les utilisent déjà.
        epf: {
          pink: "#C6122E",        // rouge principal EPF (boutons, accents actifs)
          "pink-dark": "#8E0F24", // rouge foncé (hover)
          "pink-light": "#FBE6E9",// rouge très clair (fonds, surlignage léger)
          purple: "#3B1E5E",      // violet du dégradé du logo
          dark: "#1F1B24",        // fond sombre du dashboard après connexion
          "dark-soft": "#2A2530", // fond des cartes en thème sombre
          gray: "#6B6B76",
        },
      },
      backgroundImage: {
        "epf-gradient": "linear-gradient(135deg, #3B1E5E 0%, #C6122E 100%)",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        xl2: "1.25rem",
      },
    },
  },
  plugins: [],
};
