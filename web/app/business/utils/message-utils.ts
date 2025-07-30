import { AiMessage } from "@/app/types";

export class MessageUtils {
  static createAiMessage(
    content: string,
    name: string = "answer_agent"
  ): AiMessage {
    return {
      id: (Date.now() + 1).toString(),
      type: "ai",
      content,
      usage_metadata: {
        input_tokens: 0,
        output_tokens: 0,
        total_tokens: 0,
      },
      name,
    };
  }

  static createErrorMessage(): AiMessage {
    return this.createAiMessage(
      "죄송합니다. 요청을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.",
      "answer_agent"
    );
  }

  static createLoadingMessage(): AiMessage {
    return this.createAiMessage("", "temp");
  }
}
