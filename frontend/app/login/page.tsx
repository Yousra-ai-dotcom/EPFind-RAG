/**
 * Page de connexion ("/login")
 * Déclenche la connexion Microsoft Entra ID (MSAL), puis redirige vers /chat.
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
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-epf-pink-light p-8">
      <Logo size={48} />
      <p className="text-epf-gray">Connectez-vous avec votre compte Microsoft EPF</p>

      <button
        onClick={handleLogin}
        disabled={loading}
        className="rounded-xl bg-epf-pink px-8 py-3 font-semibold text-white shadow-lg shadow-epf-pink/30 transition hover:bg-epf-pink-dark disabled:opacity-60"
      >
        {loading ? "Connexion..." : "Se connecter avec Microsoft"}
      </button>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <button
        onClick={() => router.push("/chat")}
        className="text-sm text-epf-gray underline"
      >
        Continuer sans se connecter (mode démo)
      </button>
    </main>
  );
}
