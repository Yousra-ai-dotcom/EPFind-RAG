/**
 * Page Chat ("/chat") — façon Claude : plusieurs conversations,
 * bouton "+ Nouvelle conversation", reprise d'une conversation existante,
 * sélection Module + Cours, micro, like/dislike + régénération.
 */

"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import ModuleCourseSelect from "@/components/ModuleCourseSelect";
import VoiceButton from "@/components/VoiceButton";
import Chat, { ChatMessage } from "@/components/Chat";
import { askQuestion, getMe } from "@/lib/api";
import {
  StoredConversation,
  listConversations,
  createConversation,
  addMessage,
  setMessageFeedback,
  replaceMessage,
} from "@/lib/conversations";

function ChatPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [conversations, setConversations] = useState<StoredConversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [module, setModule] = useState("");
  const [course, setCourse] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState<{
    name: string;
    email: string;
    microsoft_id: string;
  } | null>(null);

  useEffect(() => {
    async function loadUser() {
      try {
        const result = await getMe();
        console.log("Résultat /me :", result);
        setCurrentUser(result.user);
      } catch (error) {
        console.error("Erreur /me :", error);
      }
    }

    loadUser();
  }, []);

  const active = conversations.find((c) => c.id === activeId) || null;
  const messages: ChatMessage[] = active?.messages || [];

  // Charge la liste des conversations au démarrage, et ouvre celle demandée
  // dans l'URL (venant de la page Historique) ou en crée une nouvelle.
  useEffect(() => {
    const all = listConversations();
    setConversations(all);

    const requestedId = searchParams.get("conversation");

    if (requestedId && all.find((c) => c.id === requestedId)) {
      setActiveId(requestedId);
    } else if (all.length > 0) {
      setActiveId(all[0].id);
    } else {
      handleNewConversation();
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function refresh() {
    setConversations(listConversations());
  }

  function handleNewConversation() {
    const conv = createConversation();
    setConversations(listConversations());
    setActiveId(conv.id);
    setModule("");
    setCourse("");
    router.replace("/chat");
  }

  function handleOpenConversation(id: string) {
    const conv = conversations.find((c) => c.id === id);
    setActiveId(id);
    setModule(conv?.module || "");
    setCourse(conv?.course || "");
  }

  async function sendQuestion(text: string) {
    if (!text.trim() || !activeId) return;

    addMessage(activeId, { role: "user", content: text });
    refresh();
    setQuestion("");
    setLoading(true);

    try {
      const result = await askQuestion(
        text,
        module || undefined,
        course || undefined,
      );

      addMessage(activeId, {
        role: "assistant",
        content: result.answer,
        sources: result.sources,
        liked: null,
      });
    } catch {
      addMessage(activeId, {
        role: "assistant",
        content: "Une erreur est survenue, réessaie.",
      });
    } finally {
      refresh();
      setLoading(false);
    }
  }

  function handleAsk() {
    sendQuestion(question);
  }

  function handleFeedback(messageIndex: number, liked: boolean | null) {
    if (!activeId) return;

    setMessageFeedback(activeId, messageIndex, liked);
    refresh();
  }

  async function handleRegenerate(messageIndex: number) {
    if (!activeId || !active) return;

    const lastQuestion = active.messages[messageIndex - 1]?.content;

    if (!lastQuestion) return;

    setLoading(true);

    try {
      const result = await askQuestion(
        lastQuestion,
        module || undefined,
        course || undefined,
      );

      replaceMessage(activeId, messageIndex, {
        role: "assistant",
        content: result.answer,
        sources: result.sources,
        liked: null,
      });
    } catch {
      // En cas d'erreur, on laisse l'ancienne réponse telle quelle.
    } finally {
      refresh();
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      {/* Mini-colonne des conversations, façon Claude */}
      <div className="flex w-56 flex-col border-r border-epf-pink-light bg-white p-3">
        <button
          onClick={handleNewConversation}
          className="mb-3 rounded-xl bg-epf-pink px-3 py-2 text-xs font-semibold text-white hover:bg-epf-pink-dark"
        >
          + Nouvelle conversation
        </button>

        <div className="flex flex-1 flex-col gap-1 overflow-y-auto">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => handleOpenConversation(c.id)}
              className={`truncate rounded-lg px-3 py-2 text-left text-xs ${
                c.id === activeId
                  ? "bg-epf-pink-light font-semibold text-epf-pink-dark"
                  : "text-epf-gray hover:bg-epf-pink-light/50"
              }`}
            >
              {c.title}
            </button>
          ))}
        </div>
      </div>

      <main className="flex flex-1 flex-col p-6">
        <div className="mb-4 flex items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold text-epf-dark">
              💬 Chat avec vos cours
            </h1>

            {currentUser && (
              <div className="mt-1 text-sm text-epf-gray">
                Connectée : <strong>{currentUser.name}</strong> —{" "}
                {currentUser.email}
              </div>
            )}
          </div>

          <ModuleCourseSelect
            module={module}
            course={course}
            onModuleChange={setModule}
            onCourseChange={setCourse}
          />
        </div>

        <Chat
          messages={messages}
          onFeedback={handleFeedback}
          onRegenerate={handleRegenerate}
        />

        <div className="mt-4 flex gap-2">
          <input
            className="flex-1 rounded-xl border border-epf-pink-light bg-white px-4 py-3 text-sm focus:border-epf-pink focus:outline-none"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Pose ta question sur tes cours EPF..."
          />

          <VoiceButton onTranscribed={(text) => sendQuestion(text)} />

          <button
            className="rounded-xl bg-epf-pink px-6 py-3 text-sm font-semibold text-white transition hover:bg-epf-pink-dark disabled:opacity-60"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "..." : "Envoyer"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense
      fallback={
        <div className="flex h-screen items-center justify-center">
          Chargement...
        </div>
      }
    >
      <ChatPageContent />
    </Suspense>
  );
}