/**
 * Préférences utilisateur (thème + langue), partagées par toutes les pages.
 * Stockées dans le navigateur (localStorage) : elles survivent au rechargement.
 * Pas de bibliothèque externe : un mini "store" + useSyncExternalStore (React 18).
 */

"use client";

import { useEffect, useSyncExternalStore } from "react";

export type Theme = "light" | "dark";
export type Language = "fr" | "en";

const THEMES: readonly Theme[] = ["light", "dark"];
const LANGUAGES: readonly Language[] = ["fr", "en"];

const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
  listeners.add(listener);
  window.addEventListener("storage", listener); // synchronise les autres onglets
  return () => {
    listeners.delete(listener);
    window.removeEventListener("storage", listener);
  };
}

function read<T extends string>(key: string, allowed: readonly T[], fallback: T): T {
  try {
    const value = localStorage.getItem(key);
    return allowed.includes(value as T) ? (value as T) : fallback;
  } catch {
    return fallback; // stockage indisponible : valeur par défaut
  }
}

function write(key: string, value: string) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // stockage indisponible : on ignore
  }
  listeners.forEach((listener) => listener()); // prévient tous les composants
}

export function useTheme() {
  const theme = useSyncExternalStore<Theme>(
    subscribe,
    () => read("epf-theme", THEMES, "light"),
    () => "light" // valeur côté serveur
  );
  return { theme, setTheme: (value: Theme) => write("epf-theme", value) };
}

export function useLanguage() {
  const language = useSyncExternalStore<Language>(
    subscribe,
    () => read("epf-language", LANGUAGES, "fr"),
    () => "fr"
  );
  return { language, setLanguage: (value: Language) => write("epf-language", value) };
}

/** À appeler une fois dans la Sidebar : applique le thème et la langue à la page. */
export function useApplyPreferences() {
  const { theme } = useTheme();
  const { language } = useLanguage();

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);
}