"""
Tests — Génération / LLM 
 tester prompts.py (formatage) et quiz_generator (parsing JSON).
"""

from unittest.mock import patch

from generation.answer import build_answer
from generation.quiz_generator import generate_quiz


def test_build_answer_with_chunks():
    fake_chunks = [
        {
            "text": "La regression lineaire est une methode statistique...",
            "course": "Machine Learning",
            "chapter": "Regression",
            "page": 12,
        },
    ]

    with patch("generation.answer.call_llm", return_value="Voici la reponse generee"):
        result = build_answer("Explique la regression lineaire", fake_chunks)

    assert result["answer"] == "Voici la reponse generee"
    assert result["sources"] == [
        {"course": "Machine Learning", "chapter": "Regression", "page": 12}
    ]


def test_build_answer_without_chunks():
    with patch("generation.answer.call_llm", return_value="Je ne trouve pas cette information dans les cours."):
        result = build_answer("Une question hors des cours EPF", [])

    assert result["sources"] == []
    assert "ne trouve pas" in result["answer"]


def test_generate_quiz_returns_parsed_questions():
    fake_json_response = """
    [
        {
            "question": "Qu'est-ce qu'un embedding ?",
            "options": ["Une representation vectorielle", "Une base de donnees", "Un protocole reseau", "Un compilateur"],
            "correct_answer": 0,
            "explanation": "Un embedding represente un texte sous forme de vecteur numerique."
        }
    ]
    """

    with patch("generation.quiz_generator.call_llm", return_value=fake_json_response):
        questions = generate_quiz("Contenu du cours sur les embeddings", n_questions=1)

    assert len(questions) == 1
    assert questions[0]["correct_answer"] == 0
    assert len(questions[0]["options"]) == 4


def test_generate_quiz_raises_error_on_invalid_json():
    with patch("generation.quiz_generator.call_llm", return_value="ceci n'est pas du JSON"):
        try:
            generate_quiz("Contenu du cours", n_questions=1)
            raise AssertionError("Une ValueError aurait du etre levee")
        except ValueError:
            pass