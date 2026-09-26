/**
 * Client API — appelle le backend FastAPI.
 * Toutes les fonctions ajoutent automatiquement le token Microsoft
 * (si l'utilisateur est connecté) dans le header Authorization.
 */

import { getAccessToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function authHeaders(json = true): Promise<Record<string, string>> {
  const token = await getAccessToken();
  const headers: Record<string, string> = {};

  if (json) headers["Content-Type"] = "application/json";
  if (token) headers["Authorization"] = `Bearer ${token}`;

  return headers;
}

async function handle(response: Response) {
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`Erreur API (${response.status}) : ${text}`);
  }

  return response.json();
}

export type Source = {
  module?: string;
  course: string;
  document?: string;
  page: number;
};

// ---------- Chat (RAG) ----------

export async function askQuestion(
  question: string,
  module?: string,
  course?: string
): Promise<{ answer: string; sources: Source[] }> {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({
      question,
      module: module || null,
      course: course || null,
    }),
  });

  return handle(response);
}

// ---------- Révision ----------

export async function generateSummary(
  course: string,
  summaryType: string,
  module?: string
) {
  const response = await fetch(`${API_URL}/summarize`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({
      course,
      module: module || null,
      summary_type: summaryType,
    }),
  });

  return handle(response);
}

// ---------- Quiz ----------

export async function generateQuiz(
  course: string,
  level: string,
  nQuestions: number
) {
  const response = await fetch(`${API_URL}/quiz`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({
      course,
      level,
      n_questions: nQuestions,
    }),
  });

  return handle(response);
}

export async function submitQuiz(quizId: number, answers: number[]) {
  const response = await fetch(`${API_URL}/quiz/${quizId}/submit`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({ answers }),
  });

  return handle(response);
}

// ---------- Cours ----------

export async function getCourses(): Promise<{
  courses: string[];
  modules: Record<string, string[]>;
}> {
  const response = await fetch(`${API_URL}/courses`, {
    headers: await authHeaders(),
  });

  return handle(response);
}

// ---------- Historique ----------

export async function getHistory(): Promise<{
  conversations: { id: number; title: string; created_at: string }[];
}> {
  const response = await fetch(`${API_URL}/history`, {
    headers: await authHeaders(),
  });

  return handle(response);
}

export async function getConversation(conversationId: number) {
  const response = await fetch(`${API_URL}/history/${conversationId}`, {
    headers: await authHeaders(),
  });

  return handle(response);
}

// ---------- Feedback (like/dislike) ----------

export async function sendFeedback(
  question: string,
  answer: string,
  liked: boolean,
  reason?: string
) {
  const response = await fetch(`${API_URL}/feedback`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({
      question,
      answer,
      liked,
      reason: reason || null,
    }),
  });

  return handle(response);
}

// ---------- Vocal (Azure Speech) ----------

/** Envoie l'audio enregistré par le micro, reçoit le texte reconnu. */
export async function transcribeAudio(
  audioBlob: Blob
): Promise<{ text: string }> {
  const token = await getAccessToken();
  const formData = new FormData();

  formData.append("file", audioBlob, "question.webm");

  const headers: Record<string, string> = {};

  if (token) headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(`${API_URL}/speech/transcribe`, {
    method: "POST",
    headers,
    body: formData,
  });

  return handle(response);
}

/** Envoie du texte, reçoit un fichier audio (mp3) jouable directement. */
export async function synthesizeSpeech(
  text: string,
  language = "fr-FR"
): Promise<Blob> {
  const response = await fetch(`${API_URL}/speech/synthesize`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({ text, language }),
  });

  if (!response.ok) {
    throw new Error(`Erreur synthèse vocale (${response.status})`);
  }

  return response.blob();
}

// ---------- Authentification ----------

export async function getMe() {
  const response = await fetch(`${API_URL}/me`, {
    headers: await authHeaders(),
  });

  return handle(response);
}