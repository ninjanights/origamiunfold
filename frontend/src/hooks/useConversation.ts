"use client";

import { useContext } from "react";
import { ConversationContext } from "@/context/ConversationProvider";

export function useConversation() {
  const context = useContext(ConversationContext);

  if (!context) {
    throw new Error("useConversation must be used inside ConversationProvider");
  }

  return context;
}
