/**
 * Page de connexion ("/login")
 * Déclenche la connexion Microsoft Entra ID (MSAL), puis redirige vers /chat.
 * La connexion est obligatoire : pas de mode invité/démo.
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Logo from "@/components/Logo";
import { loginWithMicrosoft } from "@/lib/auth";

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleLogin() {
    setLoading(true);
    setError("");
    try {
      const account = await loginWithMicrosoft();
      if (account) {
        router.push("/chat");
      }
    } catch (err) {
      setError("La connexion a échoué. Réessayez.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-gradient-to-br from-epf-purple to-epf-pink p-8">
      <div className="rounded-2xl bg-white/95 p-10 shadow-xl">
        <div className="flex flex-col items-center gap-6">
          <Logo size={48} />
          <p className="text-center text-epf-gray">
            EPFind est réservé aux étudiants de l&apos;EPF.
            <br />
            Connectez-vous avec votre compte Microsoft EPF pour continuer.
          </p>

          <button
            onClick={handleLogin}
            disabled={loading}
            className="rounded-xl bg-epf-pink px-8 py-3 font-semibold text-white shadow-lg shadow-epf-pink/30 transition hover:bg-epf-pink-dark disabled:opacity-60"
          >
            {loading ? "Connexion..." : "Se connecter avec Microsoft"}
          </button>

          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>
      </div>
    </main>
  );
}
