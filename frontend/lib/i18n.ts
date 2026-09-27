/**
 * Traductions FR / EN. Pour ajouter un texte : une clé dans `fr`, la même dans `en`.
 * TypeScript refuse de compiler si une clé manque dans `en`.
 */

"use client";

import { useLanguage } from "./preferences";

const fr = {
  nav_chat: "Chat",
  nav_courses: "Mes cours",
  nav_revision: "Révision",
  nav_quiz: "QCM",
  nav_history: "Historique",
  nav_profile: "Mon profil",
  nav_logout: "Déconnexion",

  common_loading: "Chargement...",
  common_error: "Une erreur est survenue.",
  common_retry: "Réessayer",
  common_close: "Fermer",

  courses_title: "Mes cours",
  courses_search: "Rechercher un cours...",
  courses_loading: "Chargement des cours...",
  courses_error: "Impossible de charger les cours. Le serveur ne répond pas.",
  courses_empty: "Aucun cours disponible pour le moment.",
  courses_no_match: "Aucun cours ne correspond à « {search} ».",
  courses_card_sub: "Cours indexé dans EPFind",
  courses_choose_module: "Choisissez d'abord un module",
  courses_module_label: "Module",
  courses_open: "Ouvrir",

  history_title: "Historique",
  history_loading: "Chargement de l'historique...",
  history_error: "Impossible de charger l'historique. Le serveur ne répond pas.",
  history_empty: "Aucune conversation pour le moment.",
  history_filter_all: "Tout",
  history_filter_chat: "Chat",
  history_filter_revision: "Révision",
  history_filter_quiz: "QCM",
  history_choose_filter: "Choisissez d'abord un type d'historique",

  profile_title: "Mon profil",
  profile_theme: "Thème",
  profile_theme_light: "Clair",
  profile_theme_dark: "Sombre",
  profile_theme_aria: "Basculer le thème clair / sombre",
  profile_language: "Langue",
  profile_cgu: "Conditions générales d'utilisation",
  profile_logout: "Déconnexion",

  cgu_title: "Conditions générales d'utilisation",
  cgu_p1:
    "EPFind est un prototype réalisé dans le cadre d'un hackathon. Les réponses sont générées par une IA à partir des cours indexés : elles peuvent contenir des erreurs et doivent être vérifiées avec les supports officiels.",
  cgu_p2:
    "Les conversations sont conservées pour alimenter l'historique de l'utilisateur. Aucun mot de passe n'est stocké : la connexion est gérée par Microsoft.",
  cgu_draft: "Texte provisoire, à remplacer par les CGU définitives.",
  cgu_back: "← Retour au profil",

  // ----- Chat -----
  chat_title: "Chat avec vos cours",
  chat_hello: "Bonjour {name} 👋",
  chat_hello_generic: "Bonjour 👋",
  chat_intro: "Que veux-tu apprendre aujourd'hui ?",
  chat_new_conversation: "+ Nouvelle conversation",
  chat_placeholder: "Pose ta question sur tes cours EPF...",
  chat_send: "Envoyer",
  chat_empty_question: "Écris d'abord ta question.",
  chat_listen: "Écouter",
  chat_listening: "Lecture...",
  chat_module_placeholder: "Module...",
  chat_course_placeholder: "Cours...",

  // ----- Révision -----
  revision_title: "Réviser un cours",
  revision_module_course: "Module et cours",
  revision_how: "Comment voulez-vous réviser ?",
  revision_type_quick: "Résumé rapide",
  revision_type_detailed: "Résumé détaillé",
  revision_type_key_points: "Points clés",
  revision_type_sheet: "Fiche de révision",
  revision_type_pedagogic: "Explication pédagogique",
  revision_generate: "Générer ma fiche de révision",
  revision_generating: "Génération...",
  revision_done: "✅ Fiche de révision générée !",
  revision_empty_course: "Choisis d'abord un module et un cours.",
  revision_error: "Une erreur est survenue, réessayez.",

  // ----- Quiz -----
  quiz_title: "Créer un QCM",
  quiz_module_course: "Module et cours",
  quiz_level: "Niveau",
  quiz_level_easy: "Facile",
  quiz_level_medium: "Moyen",
  quiz_level_hard: "Difficile",
  quiz_n_questions: "Nombre de questions",
  quiz_start: "Commencer",
  quiz_starting: "Génération du QCM...",
  quiz_empty_course: "Choisis d'abord un module et un cours.",
  quiz_error: "Impossible de générer le QCM pour ce cours. Réessayez.",
  quiz_question_of: "Question {current} / {total}",
  quiz_validate: "Valider",
  quiz_correct: "✓ Correct !",
  quiz_incorrect: "✗ Incorrect",
  quiz_next: "Question suivante",
  quiz_see_score: "Voir le score",
  quiz_finished: "🎉 Test terminé",
  quiz_restart: "Refaire un QCM",
};

export type TKey = keyof typeof fr;

const en: Record<TKey, string> = {
  nav_chat: "Chat",
  nav_courses: "My courses",
  nav_revision: "Revision",
  nav_quiz: "Quiz",
  nav_history: "History",
  nav_profile: "My profile",
  nav_logout: "Log out",

  common_loading: "Loading...",
  common_error: "Something went wrong.",
  common_retry: "Retry",
  common_close: "Close",

  courses_title: "My courses",
  courses_search: "Search a course...",
  courses_loading: "Loading courses...",
  courses_error: "Unable to load courses. The server is not responding.",
  courses_empty: "No course available yet.",
  courses_no_match: "No course matches \"{search}\".",
  courses_card_sub: "Course indexed in EPFind",
  courses_choose_module: "Choose a module first",
  courses_module_label: "Module",
  courses_open: "Open",

  history_title: "History",
  history_loading: "Loading history...",
  history_error: "Unable to load history. The server is not responding.",
  history_empty: "No conversation yet.",
  history_filter_all: "All",
  history_filter_chat: "Chat",
  history_filter_revision: "Revision",
  history_filter_quiz: "Quiz",
  history_choose_filter: "Choose a history type first",

  profile_title: "My profile",
  profile_theme: "Theme",
  profile_theme_light: "Light",
  profile_theme_dark: "Dark",
  profile_theme_aria: "Toggle light / dark theme",
  profile_language: "Language",
  profile_cgu: "Terms of use",
  profile_logout: "Log out",

  cgu_title: "Terms of use",
  cgu_p1:
    "EPFind is a prototype built for a hackathon. Answers are generated by an AI from the indexed courses: they may contain mistakes and must be checked against the official course material.",
  cgu_p2:
    "Conversations are kept to build the user's history. No password is stored: sign-in is handled by Microsoft.",
  cgu_draft: "Provisional text, to be replaced by the final terms.",
  cgu_back: "← Back to profile",

  chat_title: "Chat with your courses",
  chat_hello: "Hello {name} 👋",
  chat_hello_generic: "Hello 👋",
  chat_intro: "What do you want to learn today?",
  chat_new_conversation: "+ New conversation",
  chat_placeholder: "Ask a question about your EPF courses...",
  chat_send: "Send",
  chat_empty_question: "Write your question first.",
  chat_listen: "Listen",
  chat_listening: "Playing...",
  chat_module_placeholder: "Module...",
  chat_course_placeholder: "Course...",

  revision_title: "Revise a course",
  revision_module_course: "Module and course",
  revision_how: "How do you want to revise?",
  revision_type_quick: "Quick summary",
  revision_type_detailed: "Detailed summary",
  revision_type_key_points: "Key points",
  revision_type_sheet: "Revision sheet",
  revision_type_pedagogic: "Educational explanation",
  revision_generate: "Generate my revision sheet",
  revision_generating: "Generating...",
  revision_done: "✅ Revision sheet generated!",
  revision_empty_course: "Choose a module and a course first.",
  revision_error: "Something went wrong, try again.",

  quiz_title: "Create a quiz",
  quiz_module_course: "Module and course",
  quiz_level: "Level",
  quiz_level_easy: "Easy",
  quiz_level_medium: "Medium",
  quiz_level_hard: "Hard",
  quiz_n_questions: "Number of questions",
  quiz_start: "Start",
  quiz_starting: "Generating quiz...",
  quiz_empty_course: "Choose a module and a course first.",
  quiz_error: "Unable to generate the quiz for this course. Try again.",
  quiz_question_of: "Question {current} / {total}",
  quiz_validate: "Validate",
  quiz_correct: "✓ Correct!",
  quiz_incorrect: "✗ Incorrect",
  quiz_next: "Next question",
  quiz_see_score: "See score",
  quiz_finished: "🎉 Quiz finished",
  quiz_restart: "Retake a quiz",
};

const dictionaries = { fr, en };

/** Usage : const t = useT();  puis  t("nav_chat")  */
export function useT() {
  const { language } = useLanguage();
  return (key: TKey, vars?: Record<string, string | number>) => {
    let text = dictionaries[language][key];
    if (vars) {
      for (const [k, v] of Object.entries(vars)) {
        text = text.replace(`{${k}}`, String(v));
      }
    }
    return text;
  };
}
