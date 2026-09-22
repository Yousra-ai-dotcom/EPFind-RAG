/**
 * Page QCM ("/quiz") 
 *
 * - Formulaire : cours, niveau, nombre de questions, type (QCM / Vrai-Faux)
 * - Lancer le quiz -> POST /quiz
 * - Afficher les questions une par une (composant Quiz)
 * - Écran de score final
 */

"use client";

import { useState } from "react";
import { generateQuiz } from "@/lib/api";

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

  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [validated, setValidated] = useState(false);
  const [score, setScore] = useState(0);

  async function handleStart() {
    const data = await generateQuiz(course, level, nQuestions);
    setQuestions(data.questions);
    setStep("playing");
    setCurrentIndex(0);
    setScore(0);
  }

  function handleValidate() {
    setValidated(true);
    if (selectedOption === questions[currentIndex].correct_answer) {
      setScore((prev) => prev + 1);
    }
  }

  function handleNext() {
    setValidated(false);
    setSelectedOption(null);
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setStep("finished");
    }
  }

  if (step === "config") {
    return (
      <main className="p-8 max-w-md mx-auto">
        <h1 className="text-2xl font-bold mb-6">Créer un QCM</h1>

        <input
          className="border p-2 w-full mb-4"
          value={course}
          onChange={(e) => setCourse(e.target.value)}
          placeholder="Cours"
        />

        <select
          className="border p-2 w-full mb-4"
          value={level}
          onChange={(e) => setLevel(e.target.value)}
        >
          <option value="facile">Facile</option>
          <option value="moyen">Moyen</option>
          <option value="difficile">Difficile</option>
        </select>

        <input
          type="number"
          className="border p-2 w-full mb-4"
          value={nQuestions}
          onChange={(e) => setNQuestions(Number(e.target.value))}
          min={1}
          max={20}
        />

        <button
          className="rounded bg-blue-600 px-4 py-2 text-white"
          onClick={handleStart}
          disabled={!course}
        >
          Commencer
        </button>
      </main>
    );
  }

  if (step === "playing") {
    const current = questions[currentIndex];

    return (
      <main className="p-8 max-w-md mx-auto">
        <p className="text-sm text-gray-500 mb-2">
          Question {currentIndex + 1} / {questions.length}
        </p>
        <h2 className="text-xl font-semibold mb-4">{current.question}</h2>

        <div className="flex flex-col gap-2 mb-4">
          {current.options.map((option, index) => (
            <button
              key={index}
              onClick={() => !validated && setSelectedOption(index)}
              className={`border p-2 text-left rounded ${
                selectedOption === index ? "bg-blue-100 border-blue-600" : ""
              } ${
                validated && index === current.correct_answer
                  ? "bg-green-100 border-green-600"
                  : ""
              }`}
            >
              {option}
            </button>
          ))}
        </div>

        {!validated ? (
          <button
            className="rounded bg-blue-600 px-4 py-2 text-white"
            onClick={handleValidate}
            disabled={selectedOption === null}
          >
            Valider
          </button>
        ) : (
          <div>
            <p className="mb-2">
              {selectedOption === current.correct_answer
                ? "✓ Correct !"
                : "✗ Incorrect"}
            </p>
            <p className="text-sm text-gray-600 mb-4">{current.explanation}</p>
            <button
              className="rounded bg-blue-600 px-4 py-2 text-white"
              onClick={handleNext}
            >
              Question suivante
            </button>
          </div>
        )}
      </main>
    );
  }

  return (
    <main className="p-8 max-w-md mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">🎉 Test terminé</h1>
      <p className="text-xl">
        Score : {score} / {questions.length}
      </p>
    </main>
  );
}