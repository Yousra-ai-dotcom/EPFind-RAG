/**
 * Client API — appelle le backend FastAPI.
 * Responsable : Personne 3 (avec Personne 2 pour la cohérence des contrats)
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function askQuestion(question: string, course?: string, conversationId?: number) {
  // TODO: POST `${API_URL}/ask`
  throw new Error("not implemented");
}

export async function getCourses() {
  // TODO: GET `${API_URL}/courses`
  throw new Error("not implemented");
}

export async function generateQuiz(course: string, level: string, nQuestions: number) {
  // TODO: POST `${API_URL}/quiz`
  throw new Error("not implemented");
}

export async function generateSummary(course: string, summaryType: string) {
  // TODO: POST `${API_URL}/summarize`
  throw new Error("not implemented");
}

export async function getHistory() {
  // TODO: GET `${API_URL}/history`
  throw new Error("not implemented");
}
