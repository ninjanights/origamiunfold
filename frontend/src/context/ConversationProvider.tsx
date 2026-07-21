"use client";

import { createContext, useEffect, useState, type ReactNode } from "react";

import type { Source } from "@/types/chat";

export interface ConversationMessage {
  id: string;

  role: "You" | "Fox";

  content: string;

  createdAt: number;

  sources?: Source[];
}

interface ConversationContextType {
  messages: ConversationMessage[];

  addUserMessage: (question: string, id?: string) => void;

  addAssistantMessage: (answer: string, sources?: Source[]) => void;

  clearConversation: () => void;

  deleteConversation: (questionId: string) => void;
}

export const ConversationContext =
  createContext<ConversationContextType | null>(null);

export default function ConversationProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    const request = window.indexedDB.open("origami-unfold", 1);

    request.onupgradeneeded = () => {
      request.result.createObjectStore("conversation");
    };

    request.onsuccess = () => {
      const database = request.result;
      const transaction = database.transaction("conversation", "readonly");
      const savedMessages = transaction.objectStore("conversation").get("messages");

      savedMessages.onsuccess = () => {
        if (Array.isArray(savedMessages.result)) setMessages(savedMessages.result);
        setIsHydrated(true);
        database.close();
      };

      savedMessages.onerror = () => {
        setIsHydrated(true);
        database.close();
      };
    };

    request.onerror = () => setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;

    const request = window.indexedDB.open("origami-unfold", 1);

    request.onsuccess = () => {
      const database = request.result;
      const transaction = database.transaction("conversation", "readwrite");
      transaction.objectStore("conversation").put(messages, "messages");
      transaction.oncomplete = () => database.close();
    };
  }, [isHydrated, messages]);

  const addUserMessage = (question: string, id?: string) => {
    setMessages((current) => [
      ...current,
      {
        id: id ?? crypto.randomUUID(),
        role: "You",
        content: question,
        createdAt: Date.now(),
      },
    ]);
  };

  const addAssistantMessage = (answer: string, sources: Source[] = []) => {
    setMessages((current) => [
      ...current,
      {
        id: crypto.randomUUID(),
        role: "Fox",
        content: answer,
        createdAt: Date.now(),
        sources: sources.map(({ file, page }) => ({ file, page })),
      },
    ]);
  };

  const clearConversation = () => {
    setMessages([]);
  };

  const deleteConversation = (questionId: string) => {
    setMessages((current) => {
      const questionIndex = current.findIndex((message) => message.id === questionId);

      if (questionIndex === -1) return current;

      const nextMessage = current[questionIndex + 1];
      const deleteAnswer = nextMessage?.role === "Fox";

      return current.filter(
        (_, index) => index !== questionIndex && (!deleteAnswer || index !== questionIndex + 1),
      );
    });
  };

  return (
    <ConversationContext.Provider
      value={{
        messages,
        addUserMessage,
        addAssistantMessage,
        clearConversation,
        deleteConversation,
      }}
    >
      {children}
    </ConversationContext.Provider>
  );
}
