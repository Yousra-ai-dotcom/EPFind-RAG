/**
 * Mode démo : données fictives pour montrer l'interface sans backend.
 * Activé uniquement si NEXT_PUBLIC_DEMO_MODE=true dans frontend/.env.local
 * (désactivé par défaut, donc sans effet en production).
 */

export const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === "true";

export const DEMO_COURSES: string[] = [
  "Git - Les commits",
  "Bases de données",
  "Réseaux",
  "Algorithmique",
  "Cybersécurité",
  "Machine Learning",
];