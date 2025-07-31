import { BaseMessage } from "@/app/types";
import { useState } from "react";
import { Interrupt, useInterrupt } from "./use-interrupt.hook";
import { MessageUtils } from "../utils/message-utils";
import { ChatApiService } from "../services/chat-api.service";
import { StreamProcessor } from "../services/stream-processor.service";

/**Chatbot이용 및 대화를 통해 수치적 가이던스에 영향을 주는 훅 */
export const useFingarooChat = () => {
  const [messages, setMessages] = useState<BaseMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState<string | null>(null);

  const {
    isProcessing: isInterruptProcessing,
    error: interruptError,
    processInterrupt,
  } = useInterrupt();

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (isLoading || isInterruptProcessing) return; // 로딩 중이거나 인터럽트 처리 중일 때는 입력 무시
    setInput(e.target.value);
  };

  const handleInterrupt = async (
    interrupt: Interrupt,
    currentThreadId: string
  ) => {
    await processInterrupt(interrupt, currentThreadId, (data) => {
      if (data.thread_id) {
        setThreadId(data.thread_id);
      }

      setMessages(data.messages);
    });

    // 인터럽트 처리 중 에러가 발생한 경우 에러 메시지 추가
    if (interruptError) {
      const errorMessage = MessageUtils.createErrorMessage();
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>,
    directInput?: string
  ) => {
    e.preventDefault();

    const currentInput = directInput || input;
    setInput("");
    setIsLoading(true);

    try {
      // 로딩 메시지 추가
      const loadingMessage = MessageUtils.createLoadingMessage();
      setMessages((prev) => [...prev, loadingMessage]);

      let response: Response;

      if (messages.length === 0) {
        response = await ChatApiService.sendFirstChat({
          query: currentInput,
        });
      } else {
        response = await ChatApiService.sendContinueChat({
          query: currentInput,
          thread_id: threadId || "",
        });
      }

      const streamResult = await StreamProcessor.processStream(
        response,
        (data) => {
          if (data.thread_id) {
            setThreadId(data.thread_id);
          }

          setMessages(data.messages);
        }
      );

      // 인터럽트 처리
      if (streamResult.interrupt !== 0 && streamResult.threadId) {
        await handleInterrupt(streamResult.interrupt, streamResult.threadId);
      }
    } catch (error) {
      console.error("Error calling chat API:", error);

      // 에러 메시지 추가
      const errorMessage = MessageUtils.createErrorMessage();
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    isLoading: isLoading || isInterruptProcessing, // 채팅 로딩 또는 인터럽트 처리 중
    input,
    handleInputChange,
    handleSubmit,
    setInput,
    interruptError, // 인터럽트 에러 상태도 노출
  };
};
