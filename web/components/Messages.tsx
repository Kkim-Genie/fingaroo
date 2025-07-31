import { useEffect, useRef, useState } from "react";
import FlakeId from "flake-idgen";
import { cn } from "../utils/utlis";
import { MessageItem } from "./MessageItem";
import { useChat } from "@/business/hooks/use-chat.hook";
import { ToolMessage } from "@/app/types";
import StockChart from "./StockChart";

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

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <WelcomeScreen />
      </div>
    );
  }

  return (
    <div
      className={cn(
        "lg:flex lg:flex-col lg:justify-end lg:space-y-5 lg:p-3",
        "space-y-6 p-2"
      )}
    >
      {messages.map((message) => {
        if (message.type === "human" || message.type === "ai") {
          return (
            <MessageItem
              key={message.id}
              role={message.type}
              content={message.content}
            />
          );
        }
        if (
          message.type === "tool" &&
          (message as ToolMessage).tool_name === "search_stock_price"
        ) {
          const stockData = JSON.parse(message.content);
          return <StockChart key={message.id} stockData={stockData} />;
        }
      })}

      {/**로딩중일 경우 Dot Spinner 보여주기 */}
      {isLoading ? <MessageItem role="ai" content={<DotSpinner />} /> : null}
      {/**새로운 메시지 추가됐을때 스크롤 하기 위한 div */}
      <div ref={Chatref}></div>
    </div>
  );
}

const WelcomeScreen = () => {
  const { handleSubmit } = useChat();

  const exampleQuestions = [
    "나의 매매일지를 보고 피드백해줘",
    "삼성전자 주가 어떻게 됐어?",
    "더본코리아에 대해 분석해줘",
  ];

  const handleQuestionClick = (question: string) => {
    // 가짜 form event 생성해서 submit 실행
    const fakeEvent = {
      preventDefault: () => {},
    } as React.FormEvent<HTMLFormElement>;
    handleSubmit(fakeEvent, question);
  };

  return (
    <div className="max-w-md mx-auto text-center space-y-8">
      {/* 로고 및 제목 */}
      <div className="space-y-1">
        <p className="text-[#A7A7A7]" style={{ fontFamily: "Batang, serif" }}>
          Welcome
        </p>
        <h1
          className="text-4xl font-bold bg-gradient-to-r from-[#FFA162] to-[#B9ABA2] bg-clip-text text-transparent tracking-wider"
          style={{ fontFamily: "Batang, serif" }}
        >
          Fingaroo
        </h1>
        <p
          className="text-base font-semibold bg-gradient-to-r from-[#FFA162] to-[#FFA060] bg-clip-text text-transparent"
          style={{ fontFamily: "Batang, serif" }}
        >
          your finance buddy
        </p>
      </div>

      {/* 예시 질문들 */}
      <div className="space-y-3">
        {exampleQuestions.map((question, index) => (
          <button
            key={index}
            onClick={() => handleQuestionClick(question)}
            className="w-full flex items-center justify-between bg-white rounded-3xl border border-gray-200 p-4 px-6 hover:shadow-md transition-shadow duration-200 group"
          >
            <span
              className="text-[#918787] font-bold text-left"
              style={{ fontFamily: "Batang, serif" }}
            >
              “{question}
              {`"`}
            </span>
            <div className="w-8 h-8 bg-[#FFA17C] rounded-full flex items-center justify-center flex-shrink-0 ml-7 group-hover:bg-[#FF9A6B] transition-colors duration-200">
              <svg
                className="w-4 h-4 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

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
