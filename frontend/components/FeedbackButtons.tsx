/**
 * Boutons Like / Dislike sous une réponse de l'assistant.
 * Si dislike -> demande la raison -> déclenche la régénération.
 */

"use client";

import { useState } from "react";
import { sendFeedback } from "@/lib/api";

type Props = {
  question: string;
  answer: string;
  liked?: boolean | null;
  onFeedback: (liked: boolean | null) => void;
  onRegenerate: () => void;
};

export default function FeedbackButtons({
  question,
  answer,
  liked,
  onFeedback,
  onRegenerate,
}: Props) {
  const [showReasonBox, setShowReasonBox] = useState(false);
  const [reason, setReason] = useState("");

  async function handleLike() {
    onFeedback(true);
    await sendFeedback(question, answer, true).catch(() => {});
  }

  function handleDislikeClick() {
    setShowReasonBox(true);
  }

  async function confirmDislike() {
    onFeedback(false);
    await sendFeedback(question, answer, false, reason).catch(() => {});
    setShowReasonBox(false);
    setReason("");
    onRegenerate(); // on régénère automatiquement une nouvelle réponse
  }

  return (
    <div className="mt-2">
      <div className="flex items-center gap-2 text-sm">
        <button
          onClick={handleLike}
          className={`rounded-lg px-2 py-1 transition ${
            liked === true ? "bg-green-100 text-green-700" : "text-epf-gray hover:bg-epf-pink-light"
          }`}
          title="Bonne réponse"
        >
          👍
        </button>
        <button
          onClick={handleDislikeClick}
          className={`rounded-lg px-2 py-1 transition ${
            liked === false ? "bg-red-100 text-red-700" : "text-epf-gray hover:bg-epf-pink-light"
          }`}
          title="Mauvaise réponse"
        >
          👎
        </button>
      </div>

      {showReasonBox && (
        <div className="mt-2 flex flex-col gap-2 rounded-xl border border-epf-pink-light bg-white p-3">
          <p className="text-xs text-epf-gray">
            Qu'est-ce qui ne va pas dans cette réponse ? (optionnel)
          </p>
          <input
            className="rounded-lg border border-epf-pink-light px-3 py-1.5 text-sm"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Ex: incomplet, hors sujet, faux..."
          />
          <button
            onClick={confirmDislike}
            className="self-start rounded-lg bg-epf-pink px-3 py-1.5 text-xs font-semibold text-white hover:bg-epf-pink-dark"
          >
            Envoyer et régénérer la réponse
          </button>
        </div>
      )}
    </div>
  );
}
