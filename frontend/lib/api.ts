/**
 * Client API — appelle le backend FastAPI.
 * Toutes les fonctions ajoutent automatiquement le token Microsoft
 * (si l'utilisateur est connecté) dans le header Authorization.
 */

import { getAccessToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function authHeaders(): Promise<Record<string, string>> {
  const token = await getAccessToken();
  const headers: Record<string, string> = { "Content-Type": "application/json" };
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
  course: string;
  chapter: string;
  page: number;
};

export async function askQuestion(
  question: string,
  course?: string,
  conversationId?: number
): Promise<{ answer: string; sources: Source[]; conversation_id: number }> {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({
      question,
      course: course || null,
      conversation_id: conversationId || null,
    }),
  });
  return handle(response);
}

export async function generateSummary(course: string, summaryType: string) {
  const response = await fetch(`${API_URL}/summarize`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({ course, summary_type: summaryType }),
  });
  return handle(response);
}

export async function generateQuiz(course: string, level: string, nQuestions: number) {
  const response = await fetch(`${API_URL}/quiz`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({ course, level, n_questions: nQuestions }),
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

export async function getCourses(): Promise<{ courses: string[] }> {
  const response = await fetch(`${API_URL}/courses`, {
    headers: await authHeaders(),
  });
  return handle(response);
}

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
