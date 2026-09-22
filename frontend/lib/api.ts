/**
 * Client API — appelle le backend FastAPI.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function askQuestion(
  question: string,
  course?: string,
  conversationId?: number
) {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      course,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    throw new Error("Erreur lors de l'appel a l'API /ask");
  }

  return response.json();
}



export async function generateSummary(course: string, summaryType: string) {
  const response = await fetch(`${API_URL}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      course,
      summary_type: summaryType,
    }),
  });

  if (!response.ok) {
    throw new Error("Erreur lors de l'appel a l'API /summarize");
  }

  return response.json();
}





export async function generateQuiz(
  course: string,
  level: string,
  nQuestions: number
) {
  const response = await fetch(`${API_URL}/quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      course,
      level,
      n_questions: nQuestions,
    }),
  });

  if (!response.ok) {
    throw new Error("Erreur lors de l'appel a l'API /quiz");
  }

  return response.json();
}











export async function getCourses() {
  // TODO: GET `${API_URL}/courses`
  throw new Error("not implemented");
}







export async function getHistory() {
  // TODO: GET `${API_URL}/history`
  throw new Error("not implemented");
}
