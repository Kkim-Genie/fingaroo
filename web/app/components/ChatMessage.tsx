import React from "react";

interface ChatMessageProps {
  message: string;
  type: "human" | "ai" | "system" | "tool_call" | "tool";
}

export default function ChatMessage({ message, type }: ChatMessageProps) {
  if (type !== "human" && type !== "ai") {
    return null;
  }

  return (
    <div
      className={`flex ${
        type === "human" ? "justify-end" : "justify-start"
      } mb-4`}
    >
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-3 ${
          type === "human"
            ? "bg-gradient-to-r from-blue-500 to-blue-600 text-white"
            : "bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800"
        }`}
      >
        <div className="text-sm leading-relaxed">{message}</div>
      </div>
    </div>
  );
}
