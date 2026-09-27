/**
 * Page Chat ("/chat") — plusieurs conversations (vrai historique backend
 * PostgreSQL désormais, plus de stockage local), sélection Module + Cours,
 * micro, like/dislike + régénération, salutation avec le prénom de l'étudiant.
 */

"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import ModuleCourseSelect from "@/components/ModuleCourseSelect";
import VoiceButton from "@/components/VoiceButton";
import Toast from "@/components/Toast";
import Chat, { ChatMessage } from "@/components/Chat";
import { askQuestion, getHistory, getConversation, HistoryItem } from "@/lib/api";
import { getFirstName } from "@/lib/auth";
import { useT } from "@/lib/i18n";

function ChatPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const t = useT();

  const [conversations, setConversations] = useState<HistoryItem[]>([]);
  const [activeId, setActiveId] = useState<number | undefined>(undefined);
  const [module, setModule] = useState("");
  const [course, setCourse] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState("");
  const [firstName, setFirstName] = useState("");

  function refreshConversationList() {
    getHistory("chat")
      .then((data) => setConversations(data.conversations))
      .catch(() => setConversations([]));
  }

  // Charge le prénom de l'étudiant connecté, la liste des conversations,
  // et ouvre celle demandée dans l'URL (venant de l'Historique ou de "Mes cours").
  useEffect(() => {
    setFirstName(getFirstName());
    refreshConversationList();

    const requestedId = searchParams.get("conversation");
    const requestedCourse = searchParams.get("course");
    const requestedModule = searchParams.get("module");

    if (requestedCourse) setCourse(requestedCourse);
    if (requestedModule) setModule(requestedModule);

    if (requestedId) {
      const id = Number(requestedId);
      setActiveId(id);
      getConversation(id)
        .then((data) => {
          setMessages(
            data.messages.map((m: { role: "user" | "assistant"; content: string }) => ({
              role: m.role,
              content: m.content,
            }))
          );
        })
        .catch(() => setMessages([]));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleNewConversation() {
    setActiveId(undefined);
    setMessages([]);
    router.replace("/chat");
  }

  function handleOpenConversation(id: number) {
    setActiveId(id);
    getConversation(id)
      .then((data) => {
        setMessages(
          data.messages.map((m: { role: "user" | "assistant"; content: string }) => ({
            role: m.role,
            content: m.content,
          }))
        );
      })
      .catch(() => setMessages([]));
  }

  async function sendQuestion(text: string) {
    if (!text.trim()) {
      setToast(t("chat_empty_question"));
      return;
    }

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setQuestion("");
    setLoading(true);

    try {
      const result = await askQuestion(text, module || undefined, course || undefined, activeId);
      setActiveId(result.conversation_id); // 1ère question : le backend vient de créer la conversation
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.answer, sources: result.sources, liked: null },
      ]);
      refreshConversationList();
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Une erreur est survenue, réessaie." }]);
    } finally {
      setLoading(false);
    }
  }

  function handleAsk() {
    sendQuestion(question);
  }

  function handleFeedback(messageIndex: number, liked: boolean | null) {
    setMessages((prev) => prev.map((m, i) => (i === messageIndex ? { ...m, liked } : m)));
  }

  async function handleRegenerate(messageIndex: number) {
    const lastQuestion = messages[messageIndex - 1]?.content;
    if (!lastQuestion) return;

    setLoading(true);
    try {
      const result = await askQuestion(lastQuestion, module || undefined, course || undefined, activeId);
      setMessages((prev) =>
        prev.map((m, i) =>
          i === messageIndex
            ? { role: "assistant", content: result.answer, sources: result.sources, liked: null }
            : m
        )
      );
    } catch {
      // en cas d'erreur, on laisse l'ancienne réponse telle quelle
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen bg-[#f7f6fa]">
      <Sidebar />

      <div className="flex w-56 flex-col border-r border-epf-pink-light bg-white p-3">
        <button
          onClick={handleNewConversation}
          className="mb-3 rounded-xl bg-epf-pink px-3 py-2 text-xs font-semibold text-white hover:bg-epf-pink-dark"
        >
          {t("chat_new_conversation")}
        </button>
        <div className="flex flex-1 flex-col gap-1 overflow-y-auto">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => c.id && handleOpenConversation(c.id)}
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
        <div className="mb-2 flex items-center justify-between">
          <h1 className="text-xl font-bold text-epf-dark">💬 {t("chat_title")}</h1>
          <ModuleCourseSelect
            module={module}
            course={course}
            onModuleChange={setModule}
            onCourseChange={setCourse}
          />
        </div>

        {course && (
          <p className="mb-2 text-xs font-medium text-epf-pink-dark">
            📘 Cours sélectionné : {course} {module ? `(module ${module})` : ""}
          </p>
        )}

        {messages.length === 0 && (
          <p className="mb-2 text-sm text-epf-gray">
            {firstName ? t("chat_hello", { name: firstName }) : t("chat_hello_generic")} —{" "}
            {t("chat_intro")}
          </p>
        )}

        <Chat messages={messages} onFeedback={handleFeedback} onRegenerate={handleRegenerate} />

        <div className="mt-4 flex gap-2">
          <input
            className="flex-1 rounded-xl border border-epf-pink-light bg-white px-4 py-3 text-sm focus:border-epf-pink focus:outline-none"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder={t("chat_placeholder")}
          />
          <VoiceButton onTranscribed={(text) => sendQuestion(text)} />
          <button
            className="rounded-xl bg-epf-pink px-6 py-3 text-sm font-semibold text-white transition hover:bg-epf-pink-dark disabled:opacity-60"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "..." : t("chat_send")}
          </button>
        </div>
      </main>

      {toast && <Toast message={toast} type="error" onClose={() => setToast("")} />}
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense>
      <ChatPageContent />
    </Suspense>
  );
}
