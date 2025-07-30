import { useContext } from "react";
import { ChatContext } from "./provider/chat-provider";
import { ChatProviderProps } from "@/app/types";

export function useChat(): ChatProviderProps {
  const chat = useContext(ChatContext);
  if (!chat) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return chat;
}
