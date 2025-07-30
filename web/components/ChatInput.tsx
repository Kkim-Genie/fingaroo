/* eslint-disable @typescript-eslint/no-explicit-any */
import { useChat } from "@/business/hooks/use-chat.hook";
import React, { useEffect, useRef } from "react";

export default function ChatInput() {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { input, handleInputChange, handleSubmit, isLoading } = useChat();

  useEffect(() => {
    if (!isLoading) {
      textareaRef.current?.focus();
    }
  }, [isLoading]);

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-gray-200 bg-white py-2 px-4"
    >
      <div className="flex items-end gap-3">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            rows={1}
            className="w-full resize-none overflow-y-auto border-none p-0 px-1 text-lg scrollbar-thin focus:border-white focus:shadow-none focus:ring-0"
            placeholder="무엇이든 물어보세요."
            disabled={isLoading}
            style={{
              height: "auto",
              overflowY: "auto",
            }}
            // 채팅 입력 시 높이 자동 조절 (로딩 중일 때는 무시)
            onInput={(e) => {
              if (isLoading) return;
              const target = e.target as HTMLTextAreaElement;
              target.style.height = "auto";
              const maxHeight = 72;
              target.style.height = `${Math.min(
                target.scrollHeight,
                maxHeight
              )}px`;
            }}
            // 엔터키로 submit 실행
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                if (!isLoading && input.trim() !== "") {
                  handleSubmit(e as any);
                }
              }
            }}
          />
        </div>
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
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
