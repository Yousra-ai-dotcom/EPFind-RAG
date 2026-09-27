/**
 * Page Profil ("/profile")
 * Thème et langue : appliqués à tout le site et mémorisés dans le navigateur.
 * Nom et email : ceux du compte Microsoft EPF connecté (plus de données fictives).
 */

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import { getEmail, getFirstName, logout } from "@/lib/auth";
import { useT } from "@/lib/i18n";
import { useTheme, useLanguage, Language } from "@/lib/preferences";

export default function ProfilePage() {
  const { theme, setTheme } = useTheme();
  const { language, setLanguage } = useLanguage();
  const router = useRouter();
  const t = useT();
  const dark = theme === "dark";

  const [firstName, setFirstName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    setFirstName(getFirstName());
    setEmail(getEmail());
  }, []);

  const displayName = firstName || t("profile_title");
  const displayInitial = (firstName || "E").charAt(0).toUpperCase();

  async function handleLogout() {
    try {
      await logout();
    } catch {
      // mode démo : pas de session à fermer
    }
    router.push("/login");
  }

  const card = "rounded-xl2 bg-white p-5 shadow-sm";

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-6">
        <h1 className="mb-6 text-xl font-bold text-epf-dark">👤 {t("profile_title")}</h1>

        <div className="flex max-w-xl flex-col gap-4">
          {/* Identité */}
          <section className={`flex items-center gap-4 ${card}`}>
            <span className="flex h-14 w-14 items-center justify-center rounded-full bg-epf-pink text-xl font-bold text-white">
              {displayInitial}
            </span>
            <div>
              <p className="font-semibold text-epf-dark">{displayName}</p>
              <p className="text-sm text-epf-gray">{email || "—"}</p>
            </div>
          </section>

          {/* Thème */}
          <section className={`flex items-center justify-between ${card}`}>
            <div>
              <p className="text-sm font-semibold text-epf-dark">{t("profile_theme")}</p>
              <p className="text-xs text-epf-gray">
                {dark ? t("profile_theme_dark") : t("profile_theme_light")}
              </p>
            </div>
            <button
              role="switch"
              aria-checked={dark}
              aria-label={t("profile_theme_aria")}
              onClick={() => setTheme(dark ? "light" : "dark")}
              className={`relative h-7 w-12 rounded-full transition-colors ${
                dark ? "bg-epf-pink" : "bg-gray-300"
              }`}
            >
              <span
                className={`absolute top-1 h-5 w-5 rounded-full bg-white transition-all ${
                  dark ? "left-6" : "left-1"
                }`}
              />
            </button>
          </section>

          {/* Langue */}
          <section className={card}>
            <label
              className="mb-2 block text-sm font-semibold text-epf-dark"
              htmlFor="language"
            >
              {t("profile_language")}
            </label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value as Language)}
              className="w-full rounded-xl border border-epf-pink-light bg-white px-4 py-2.5 text-sm text-epf-dark focus:border-epf-pink focus:outline-none"
            >
              <option value="fr">Français</option>
              <option value="en">English</option>
            </select>
          </section>

          {/* CGU + Déconnexion */}
          <section className={`flex items-center justify-between ${card}`}>
            <Link href="/cgu" className="text-sm font-medium text-epf-pink underline">
              {t("profile_cgu")}
            </Link>
            <button
              onClick={handleLogout}
              className="rounded-xl bg-epf-pink px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-epf-pink-dark"
            >
              {t("profile_logout")}
            </button>
          </section>
        </div>
      </main>
    </div>
  );
}