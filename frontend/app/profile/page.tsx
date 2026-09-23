/**
 * Page Profil ("/profile")
 * Thème et langue : purement visuels pour la démo (rien n'est sauvegardé).
 * Nom et email : données fictives en attendant le compte Microsoft.
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import { logout } from "@/lib/auth";

const FAKE_USER = { name: "Étudiant EPF", email: "prenom.nom@epfedu.fr" };

export default function ProfilePage() {
  const [dark, setDark] = useState(false);
  const [language, setLanguage] = useState("fr");
  const router = useRouter();

  async function handleLogout() {
    try {
      await logout();
    } catch {
      // mode démo : pas de session à fermer
    }
    router.push("/login");
  }

  const card = dark ? "bg-white/10" : "bg-white shadow-sm";

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <main
        className={`flex-1 overflow-y-auto p-6 transition-colors ${
          dark ? "bg-epf-dark text-white" : "bg-[#f7f6fa] text-epf-dark"
        }`}
      >
        <h1 className="mb-6 text-xl font-bold">👤 Mon profil</h1>

        <div className="flex max-w-xl flex-col gap-4">
          {/* Identité */}
          <section className={`flex items-center gap-4 rounded-xl2 p-5 ${card}`}>
            <span className="flex h-14 w-14 items-center justify-center rounded-full bg-epf-pink text-xl font-bold text-white">
              {FAKE_USER.name.charAt(0)}
            </span>
            <div>
              <p className="font-semibold">{FAKE_USER.name}</p>
              <p className="text-sm opacity-70">{FAKE_USER.email}</p>
            </div>
          </section>

          {/* Thème */}
          <section className={`flex items-center justify-between rounded-xl2 p-5 ${card}`}>
            <div>
              <p className="text-sm font-semibold">Thème</p>
              <p className="text-xs opacity-70">{dark ? "Sombre" : "Clair"}</p>
            </div>
            <button
              role="switch"
              aria-checked={dark}
              aria-label="Basculer le thème clair / sombre"
              onClick={() => setDark(!dark)}
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
          <section className={`rounded-xl2 p-5 ${card}`}>
            <label className="mb-2 block text-sm font-semibold" htmlFor="language">
              Langue
            </label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full rounded-xl border border-epf-pink-light bg-white px-4 py-2.5 text-sm text-epf-dark focus:border-epf-pink focus:outline-none"
            >
              <option value="fr">Français</option>
              <option value="en">English</option>
            </select>
          </section>

          {/* CGU + Déconnexion */}
          <section className={`flex items-center justify-between rounded-xl2 p-5 ${card}`}>
            <Link href="/cgu" className="text-sm font-medium text-epf-pink underline">
              Conditions générales d&apos;utilisation
            </Link>
            <button
              onClick={handleLogout}
              className="rounded-xl bg-epf-pink px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-epf-pink-dark"
            >
              Déconnexion
            </button>
          </section>
        </div>
      </main>
    </div>
  );
}