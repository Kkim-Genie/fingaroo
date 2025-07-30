"use client";

import { ChatProviderProps } from "@/app/types";
import { createContext } from "react";
import { useFingarooChat } from "../use-fingaroo-chat.hook";

/**Chatbot에 대한 Context */
export const ChatContext = createContext<ChatProviderProps | null>(null);

/**GPT Chatbot을 사용하기 위한 Provider */
export default function ChatProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ChatContext.Provider value={useFingarooChat()}>
      {children}
    </ChatContext.Provider>
  );
}
