import { AiMessage, BaseMessage } from "@/app/types";
import { Interrupt } from "../hooks/use-interrupt.hook";

export interface ChatResponse {
  messages: BaseMessage[];
  answer: string;
  thread_id: string;
  __interrupt__: Interrupt;
}

export interface StreamProcessorResult {
  messages: BaseMessage[];
  threadId: string | null;
  interrupt: Interrupt;
}

export class StreamProcessor {
  static async processStream(
    response: Response,
    onProgress?: (data: ChatResponse) => void
  ): Promise<StreamProcessorResult> {
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error("Response body is null");
    }

    const decoder = new TextDecoder();
    let interrupt: Interrupt = 0;
    let threadId: string | null = null;
    let lastMessages: BaseMessage[] = [];

    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      const buffer = decoder.decode(value, { stream: true });
      const bufferList = buffer.split("data:").filter((item) => item !== "");

      try {
        const data: ChatResponse = JSON.parse(
          bufferList[bufferList.length - 1].trim()
        );

        if (data.thread_id) {
          threadId = data.thread_id;
        }

        if (data.__interrupt__) {
          interrupt = data.__interrupt__;
        }

        // Process messages
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
            name: "answer_agent",
          };
          lastMessages = [...data.messages, answerMessage];
        } else {
          lastMessages = data.messages;
        }

        // Call progress callback if provided
        onProgress?.(data);
      } catch (error) {
        console.log("json parse error:", error);
      }
    }

    return {
      messages: lastMessages,
      threadId,
      interrupt,
    };
  }
}
