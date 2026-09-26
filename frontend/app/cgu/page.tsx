/**
 * Page CGU ("/cgu") - texte provisoire pour la démo.
 */

"use client";

import Link from "next/link";
import Sidebar from "@/components/Sidebar";
import { useT } from "@/lib/i18n";

export default function CguPage() {
  const t = useT();
  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">
        <h1 className="mb-6 text-xl font-bold text-epf-dark">{t("cgu_title")}</h1>
        <div className="max-w-2xl space-y-3 rounded-xl2 bg-white p-6 text-sm leading-relaxed text-epf-dark shadow-sm">
          <p>{t("cgu_p1")}</p>
          <p>{t("cgu_p2")}</p>
          <p className="text-epf-gray">{t("cgu_draft")}</p>
        </div>
        <Link href="/profile" className="mt-4 inline-block text-sm text-epf-pink underline">
          {t("cgu_back")}
        </Link>
      </main>
    </div>
  );
}