/**
 * Petite notification temporaire ("toast"), affichée en bas à droite,
 * qui disparaît automatiquement après quelques secondes.
 * Utilisée pour "génération terminée" (Révision), et pour les messages
 * de validation ("écris d'abord ta question", etc.).
 */

"use client";

import { useEffect } from "react";

type Props = {
  message: string;
  type?: "success" | "error";
  onClose: () => void;
  durationMs?: number;
};

export default function Toast({ message, type = "success", onClose, durationMs = 3000 }: Props) {
  useEffect(() => {
    const timer = setTimeout(onClose, durationMs);
    return () => clearTimeout(timer);
  }, [onClose, durationMs]);

  return (
    <div
      className={`fixed bottom-6 right-6 z-50 rounded-xl px-4 py-3 text-sm font-medium text-white shadow-lg transition ${
        type === "success" ? "bg-green-600" : "bg-epf-pink"
      }`}
    >
      {message}
    </div>
  );
}
