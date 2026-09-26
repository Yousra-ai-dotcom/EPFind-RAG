/**
 * Gestion des conversations du Chat, façon Claude : plusieurs
 * conversations, "+ Nouvelle conversation", reprendre une ancienne.
 *
 * Comme le backend n'a pas encore de vraie base de données branchée
 * (backend/database est encore un TODO côté Yousra), on stocke les
 * conversations dans le navigateur (localStorage), sur le même
 * principe que frontend/lib/preferences.ts de Diarra.
 *
 * Le jour où /history sera prêt côté backend, il suffira de remplacer
 * les fonctions ci-dessous par de vrais appels API, sans changer la
 * façon dont le Chat les utilise.
 */

"use client";

import { Source } from "./api";

export type StoredMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  liked?: boolean | null; // true = like, false = dislike, null/undefined = pas de retour
};

export type StoredConversation = {
  id: string;
  title: string;
  module?: string;
  course?: string;
  messages: StoredMessage[];
  createdAt: string;
  updatedAt: string;
};

const STORAGE_KEY = "epf-conversations";

function readAll(): StoredConversation[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function writeAll(conversations: StoredConversation[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  } catch {
    // stockage indisponible (navigation privée, quota) : on ignore
  }
}

/** Liste toutes les conversations, les plus récentes en premier. */
export function listConversations(): StoredConversation[] {
  return readAll().sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

/** Récupère une conversation précise par son id. */
export function getStoredConversation(id: string): StoredConversation | undefined {
  return readAll().find((c) => c.id === id);
}

/** Crée une nouvelle conversation vide et la retourne. */
export function createConversation(module?: string, course?: string): StoredConversation {
  const now = new Date().toISOString();
  const conversation: StoredConversation = {
    id: `local-${Date.now()}`,
    title: "Nouvelle conversation",
    module,
    course,
    messages: [],
    createdAt: now,
    updatedAt: now,
  };
  const all = readAll();
  all.push(conversation);
  writeAll(all);
  return conversation;
}

/** Ajoute un message à une conversation existante, et met à jour son titre si besoin. */
export function addMessage(conversationId: string, message: StoredMessage) {
  const all = readAll();
  const conversation = all.find((c) => c.id === conversationId);
  if (!conversation) return;

  conversation.messages.push(message);
  conversation.updatedAt = new Date().toISOString();

  // Le titre de la conversation = la première question posée
  if (conversation.title === "Nouvelle conversation" && message.role === "user") {
    conversation.title =
      message.content.length > 50 ? message.content.slice(0, 50) + "..." : message.content;
  }

  writeAll(all);
}

/** Met à jour le like/dislike d'un message précis (par son index dans la conversation). */
export function setMessageFeedback(
  conversationId: string,
  messageIndex: number,
  liked: boolean | null
) {
  const all = readAll();
  const conversation = all.find((c) => c.id === conversationId);
  if (!conversation || !conversation.messages[messageIndex]) return;

  conversation.messages[messageIndex].liked = liked;
  writeAll(all);
}

/** Remplace le contenu d'un message (utilisé pour "régénérer la réponse"). */
export function replaceMessage(conversationId: string, messageIndex: number, message: StoredMessage) {
  const all = readAll();
  const conversation = all.find((c) => c.id === conversationId);
  if (!conversation || !conversation.messages[messageIndex]) return;

  conversation.messages[messageIndex] = message;
  conversation.updatedAt = new Date().toISOString();
  writeAll(all);
}

export function deleteConversation(id: string) {
  writeAll(readAll().filter((c) => c.id !== id));
}
