export interface SourceReference {
    filename: string;
    chunkNumber: number;
    pageNumber: number;
    souce: number;
}

export interface ConversationMessage {
    id: string;

  role: "user" | "assistant";

  content: string;

  createdAt: number;

  sources?: SourceReference[];
}

export interface ConversationContextType {
  messages: ConversationMessage[];

  addUserMessage: (content: string) => void;

  addAssistantMessage: (
    content: string,
    sources?: SourceReference[],
  ) => void;

  clearConversation: () => void;
}