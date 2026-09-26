/**
 * Page QCM ("/quiz")
 */

"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import CourseSelector from "@/components/CourseSelector";
import { generateQuiz, submitQuiz } from "@/lib/api";

type Question = {
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
};

export default function QuizPage() {
  const [step, setStep] = useState<"config" | "playing" | "finished">("config");
  const [course, setCourse] = useState("");
  const [level, setLevel] = useState("facile");
  const [nQuestions, setNQuestions] = useState(10);
  const [loading, setLoading] = useState(false);

  const [quizId, setQuizId] = useState<number | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<number[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [validated, setValidated] = useState(false);
  const [finalScore, setFinalScore] = useState<{ score: number; total: number } | null>(null);

  async function handleStart() {
    setLoading(true);
    try {
      const data = await generateQuiz(course, level, nQuestions);
      setQuizId(data.quiz_id);
      setQuestions(data.questions);
      setAnswers([]);
      setStep("playing");
      setCurrentIndex(0);
    } catch {
      alert("Impossible de générer le QCM pour ce cours. Réessayez.");
    } finally {
      setLoading(false);
    }
  }

  function handleValidate() {
    setValidated(true);
  }

  async function handleNext() {
    const newAnswers = [...answers, selectedOption ?? -1];
    setAnswers(newAnswers);
    setValidated(false);
    setSelectedOption(null);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
    } else if (quizId) {
      const result = await submitQuiz(quizId, newAnswers);
      setFinalScore({ score: result.score, total: result.total });
      setStep("finished");
    }
  }

  if (step === "config") {
    return (
      <div className="flex h-screen bg-[#f7f6fa]">
        <Sidebar />
        <main className="flex-1 p-6">
          <h1 className="mb-6 text-xl font-bold text-epf-dark">📝 Créer un QCM</h1>

          <div className="max-w-md rounded-xl2 bg-white p-6 shadow-sm">
            <label className="mb-2 block text-sm font-semibold text-epf-dark">Cours</label>
            <CourseSelector value={course} onChange={setCourse} />

            <label className="mb-2 mt-4 block text-sm font-semibold text-epf-dark">Niveau</label>
            <select
              className="w-full rounded-xl border border-epf-pink-light px-4 py-2.5 text-sm"
              value={level}
              onChange={(e) => setLevel(e.target.value)}
            >
              <option value="facile">Facile</option>
              <option value="moyen">Moyen</option>
              <option value="difficile">Difficile</option>
            </select>

            <label className="mb-2 mt-4 block text-sm font-semibold text-epf-dark">
              Nombre de questions
            </label>
            <input
              type="number"
              className="w-full rounded-xl border border-epf-pink-light px-4 py-2.5 text-sm"
              value={nQuestions}
              onChange={(e) => setNQuestions(Number(e.target.value))}
              min={1}
              max={20}
            />

            <button
              className="mt-6 w-full rounded-xl bg-epf-pink py-3 text-sm font-semibold text-white transition hover:bg-epf-pink-dark disabled:opacity-60"
              onClick={handleStart}
              disabled={!course || loading}
            >
              {loading ? "Génération du QCM..." : "Commencer"}
            </button>
          </div>
        </main>
      </div>
    );
  }

  if (step === "playing") {
    const current = questions[currentIndex];
    return (
      <div className="flex h-screen bg-[#f7f6fa]">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="mx-auto max-w-xl rounded-xl2 bg-white p-6 shadow-sm">
            <p className="mb-2 text-xs font-medium text-epf-gray">
              Question {currentIndex + 1} / {questions.length}
            </p>
            <h2 className="mb-4 text-lg font-semibold text-epf-dark">{current.question}</h2>

            <div className="flex flex-col gap-2">
              {current.options.map((option, index) => {
                const isCorrect = index === current.correct_answer;
                const isSelected = selectedOption === index;
                let style = "border-epf-pink-light";
                if (validated && isCorrect) style = "border-green-500 bg-green-50";
                else if (validated && isSelected) style = "border-red-400 bg-red-50";
                else if (isSelected) style = "border-epf-pink bg-epf-pink-light";

                return (
                  <button
                    key={index}
                    onClick={() => !validated && setSelectedOption(index)}
                    className={`rounded-xl border px-4 py-2.5 text-left text-sm ${style}`}
                  >
                    {option}
                  </button>
                );
              })}
            </div>

            {!validated ? (
              <button
                className="mt-6 rounded-xl bg-epf-pink px-6 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
                onClick={handleValidate}
                disabled={selectedOption === null}
              >
                Valider
              </button>
            ) : (
              <div className="mt-6">
                <p className="mb-1 font-semibold">
                  {selectedOption === current.correct_answer ? "✓ Correct !" : "✗ Incorrect"}
                </p>
                <p className="mb-4 text-sm text-epf-gray">{current.explanation}</p>
                <button
                  className="rounded-xl bg-epf-pink px-6 py-2.5 text-sm font-semibold text-white"
                  onClick={handleNext}
                >
                  {currentIndex + 1 < questions.length ? "Question suivante" : "Voir le score"}
                </button>
              </div>
            )}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />
      <main className="flex flex-1 items-center justify-center">
        <div className="rounded-xl2 bg-white p-10 text-center shadow-sm">
          <h1 className="mb-2 text-2xl font-bold text-epf-dark">🎉 Test terminé</h1>
          <p className="text-3xl font-extrabold text-epf-pink">
            {finalScore?.score} / {finalScore?.total}
          </p>
          <button
            className="mt-6 rounded-xl bg-epf-pink px-6 py-2.5 text-sm font-semibold text-white"
            onClick={() => setStep("config")}
          >
            Refaire un QCM
          </button>
        </div>
      </main>
    </div>
  );
}
