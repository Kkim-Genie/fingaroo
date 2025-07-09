import React, { useState, useRef, useEffect } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import { AiMessage, BaseMessage } from "../types";

export default function ChatContainer() {
  const [messages, setMessages] = useState<BaseMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  console.log(messages);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: message,
          messages: messages,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("Response body is null");
      }

      const aiMessage: AiMessage = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: "",
        usage_metadata: {
          input_tokens: 0,
          output_tokens: 0,
          total_tokens: 0,
        },
        name: "temp",
      };

      // Add empty AI message to show loading
      setMessages((prev) => [...prev, aiMessage]);

      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const buffer = decoder.decode(value, { stream: true });
        const bufferList = buffer.split("data:").filter((item) => item !== "");
        const data: { messages: BaseMessage[]; answer: string } = JSON.parse(
          bufferList[bufferList.length - 1].trim()
        );

        if (data.messages[data.messages.length - 1].type !== "ai") {
          const answerMessage: AiMessage = {
            id: (Date.now() + 1).toString(),
            type: "ai",
            content: data.answer,
            usage_metadata: {
              input_tokens: 0,
              output_tokens: 0,
              total_tokens: 0,
            },
            name: "supervisor",
          };
          setMessages([...data.messages, answerMessage]);
        } else {
          setMessages(data.messages);
        }
      }
    } catch (error) {
      console.error("Error calling chat API:", error);

      // Add error message
      const errorMessage: AiMessage = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content:
          "죄송합니다. 요청을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.",
        usage_metadata: {
          input_tokens: 0,
          output_tokens: 0,
          total_tokens: 0,
        },
        name: "supervisor",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <ChatHeader />

      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message.content}
            type={message.type}
          />
        ))}

        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gradient-to-r from-gray-100 to-gray-200 rounded-2xl px-4 py-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.1s" }}
                ></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                ></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
