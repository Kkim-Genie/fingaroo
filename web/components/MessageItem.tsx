import ReactMarkdown from "react-markdown";
import styles from "./message-item.module.css";
import { cn } from "../utils/utlis";

export type MessageProps = {
  role: "human" | "ai" | "system" | "tool" | "tool_call";
  content: React.ReactNode;
};

/**기본 대화에 대한 메시지 컴포넌트 */
export const MessageItem = ({ role, content }: MessageProps) => {
  if (role === "human") {
    return (
      <div
        className={cn(
          "flex h-auto flex-col-reverse items-end justify-end whitespace-pre-wrap"
        )}
      >
        <div
          className={cn(
            "flex w-auto max-w-80 justify-end rounded-lg bg-black px-5 py-3 text-white lg:max-w-96"
          )}
        >
          <div className="flex font-pretendard text-sm font-semibold">
            {content}
          </div>
        </div>
      </div>
    );
  }
  return (
    <div
      className={cn(
        "flex h-auto flex-col-reverse items-start justify-start whitespace-pre-wrap"
      )}
    >
      <div
        className={cn(
          "flex w-auto max-w-[95%] justify-start rounded-lg bg-white px-5 py-3 text-black drop-shadow-fingoo"
        )}
      >
        <div className={cn("flex flex-col", styles.markdownContent)}>
          {typeof content === "string" ? (
            <ReactMarkdown>{content}</ReactMarkdown>
          ) : (
            content
          )}
        </div>
      </div>
    </div>
  );
};
