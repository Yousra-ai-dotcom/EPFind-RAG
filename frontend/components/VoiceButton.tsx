/**
 * Bouton micro : enregistre la voix de l'étudiant, l'envoie au backend
 * (Azure Speech-to-Text), et renvoie le texte reconnu au composant parent.
 */

"use client";

import { useRef, useState } from "react";
import { transcribeAudio } from "@/lib/api";

type Props = {
  onTranscribed: (text: string) => void;
};

export default function VoiceButton({ onTranscribed }: Props) {
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        setLoading(true);
        const audioBlob = new Blob(chunksRef.current, { type: recorder.mimeType });
        try {
          const result = await transcribeAudio(audioBlob);
          onTranscribed(result.text);
        } catch {
          alert("Impossible de reconnaître la voix, réessaie.");
        } finally {
          setLoading(false);
        }
        // Coupe le micro proprement
        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start();
      mediaRecorderRef.current = recorder;
      setRecording(true);
    } catch {
      alert("Le micro n'est pas accessible. Vérifie les autorisations du navigateur.");
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }

  return (
    <button
      type="button"
      onClick={recording ? stopRecording : startRecording}
      disabled={loading}
      title={recording ? "Arrêter l'enregistrement" : "Poser la question à l'oral"}
      className={`flex h-11 w-11 items-center justify-center rounded-xl border text-lg transition ${
        recording
          ? "border-red-400 bg-red-50 text-red-500 animate-pulse"
          : "border-epf-pink-light bg-white text-epf-pink hover:bg-epf-pink-light"
      }`}
    >
      {loading ? "⏳" : recording ? "⏹" : "🎤"}
    </button>
  );
}