/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import { ChatApiService } from "../services/chat-api.service";
import { StreamProcessor } from "../services/stream-processor.service";

type Interrupt =
  | 0
  | {
      command: string;
      payload: Record<string, any>;
    };

interface UseInterruptReturn {
  isProcessing: boolean;
  error: string | null;
  processInterrupt: (
    interrupt: Interrupt,
    threadId: string,
    onUpdate: (data: any) => void
  ) => Promise<void>;
  shouldProcessInterrupt: (interrupt: Interrupt) => boolean;
}

export const useInterrupt = (): UseInterruptReturn => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getInterruptResult = async (interrupt: Interrupt): Promise<string> => {
    if (interrupt === 0) {
      return "";
    }

    switch (interrupt.command) {
      case "add_indicator":
        return "";

      default:
        return "존재하지 않는 기능입니다.";
    }
  };

  const shouldProcessInterrupt = (interrupt: Interrupt): boolean => {
    return interrupt !== 0;
  };

  const processInterrupt = async (
    interrupt: Interrupt,
    threadId: string,
    onUpdate: (data: any) => void
  ): Promise<void> => {
    if (!shouldProcessInterrupt(interrupt)) {
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const result = await getInterruptResult(interrupt);

      const response = await ChatApiService.sendInterrupt({
        payload: { result },
        thread_id: threadId,
      });

      const streamResult = await StreamProcessor.processStream(
        response,
        onUpdate
      );

      // 재귀적으로 다음 인터럽트 처리
      if (streamResult.interrupt !== 0 && streamResult.threadId) {
        await processInterrupt(
          streamResult.interrupt,
          streamResult.threadId,
          onUpdate
        );
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Unknown error occurred";
      setError(errorMessage);
      console.error("Error processing interrupt:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  return {
    isProcessing,
    error,
    processInterrupt,
    shouldProcessInterrupt,
  };
};

export type { Interrupt };
