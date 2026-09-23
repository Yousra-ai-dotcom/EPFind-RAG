/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Couleurs inspirées du logo EPF (magenta/rose + fond sombre)
        epf: {
          pink: "#E6007E",
          "pink-dark": "#B4005F",
          "pink-light": "#FDE7F3",
          dark: "#1A1523",
          gray: "#6B6B76",
        },
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
