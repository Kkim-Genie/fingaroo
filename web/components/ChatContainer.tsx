import ChatInput from "./ChatInput";
import { Messages } from "./Messages";

export default function ChatContainer() {
  return (
    <div className="h-full flex flex-col w-full">
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        <Messages />
      </div>

      <ChatInput />
    </div>
  );
}
