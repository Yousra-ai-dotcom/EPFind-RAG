/**
 * Page CGU ("/cgu") - texte provisoire pour la démo.
 */

import Link from "next/link";
import Sidebar from "@/components/Sidebar";

export default function CguPage() {
  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">
        <h1 className="mb-6 text-xl font-bold text-epf-dark">
          Conditions générales d&apos;utilisation
        </h1>
        <div className="max-w-2xl space-y-3 rounded-xl2 bg-white p-6 text-sm leading-relaxed text-epf-dark shadow-sm">
          <p>
            EPF Find est un prototype réalisé dans le cadre d&apos;un hackathon. Les
            réponses sont générées par une IA à partir des cours indexés : elles
            peuvent contenir des erreurs et doivent être vérifiées avec les supports
            officiels.
          </p>
          <p>
            Les conversations sont conservées pour alimenter l&apos;historique de
            l&apos;utilisateur. Aucun mot de passe n&apos;est stocké : la connexion est
            gérée par Microsoft.
          </p>
          <p className="text-epf-gray">Texte provisoire, à remplacer par les CGU définitives.</p>
        </div>
        <Link href="/profile" className="mt-4 inline-block text-sm text-epf-pink underline">
          ← Retour au profil
        </Link>
      </main>
    </div>
  );
}