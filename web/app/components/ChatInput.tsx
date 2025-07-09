import React, { useState } from "react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({
  onSendMessage,
  disabled = false,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-gray-200 bg-white p-4"
    >
      <div className="flex items-end gap-3">
        <div className="flex-1 relative">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="메시지를 입력하세요..."
            disabled={disabled}
            className="w-full resize-none rounded-2xl border border-gray-200 bg-gray-50 px-4 py-3 pr-12 text-sm focus:border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-100 transition-all duration-200"
            rows={1}
            style={{ minHeight: "44px", maxHeight: "120px" }}
          />
        </div>
        <button
          type="submit"
          disabled={!message.trim() || disabled}
          className="flex-shrink-0 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 p-3 text-white shadow-lg hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:scale-105"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
    </form>
  );
}
