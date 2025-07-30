import { useEffect, useRef, useState } from "react";
import FlakeId from "flake-idgen";
import { useChat } from "../business/hooks/use-chat.hook";
import { cn } from "../utils/utlis";
import { MessageItem } from "./MessageItem";

const flake = new FlakeId();

/**chatbot과 한 대화내용들을 보여주는 컴포넌트  */
export function Messages() {
  const { messages, isLoading } = useChat();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const Chatref = useRef<HTMLDivElement | null>(null);

  const lastMessageContent = messages[messages.length - 1]?.content;

  useEffect(() => {
    if (sessionId === null) {
      const id = parseInt(flake.next().toString("hex"), 16);
      setSessionId(id);
    }
  }, []);

  useEffect(() => {
    //새로운 메시지가 추가됐을때 맨 아래로 스크롤을 내림
    Chatref.current?.scrollIntoView({ behavior: "auto" });
  }, [lastMessageContent]);

  return (
    <div
      className={cn(
        "lg:flex lg:h-full lg:flex-col lg:justify-end lg:space-y-5 lg:p-3",
        "space-y-6 p-2"
      )}
    >
      {messages.map((message) => {
        return message.type === "human" || message.type === "ai" ? (
          <MessageItem
            key={message.id}
            role={message.type}
            content={message.content}
          />
        ) : undefined;
      })}

      {/**로딩중일 경우 Dot Spinner 보여주기 */}
      {isLoading ? <MessageItem role="ai" content={<DotSpinner />} /> : null}
      {/**새로운 메시지 추가됐을때 스크롤 하기 위한 div */}
      <div ref={Chatref}></div>
    </div>
  );
}

const DotSpinner = () => (
  <div className="flex items-center justify-center space-x-2">
    <div className=" relative flex h-2 w-2 ">
      <span className=" absolute inline-flex h-full w-full animate-ping rounded-full bg-black"></span>
      <span className=" relative inline-flex h-2 w-2 rounded-full bg-gray-500"></span>
    </div>
    <div className=" relative flex h-2 w-2 ">
      <span className=" absolute inline-flex h-full w-full animate-ping rounded-full bg-black delay-150"></span>
      <span className=" relative inline-flex h-2 w-2 rounded-full bg-gray-500"></span>
    </div>
    <div className=" relative flex h-2 w-2 ">
      <span className=" absolute inline-flex h-full w-full animate-ping rounded-full bg-black delay-150"></span>
      <span className=" relative inline-flex h-2 w-2 rounded-full bg-gray-500"></span>
    </div>
  </div>
);
