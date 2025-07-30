import ChatHeader from "./ChatHeader";
import ChatInput from "./ChatInput";
import { Messages } from "./Messages";

export default function ChatContainer() {
  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <ChatHeader />

      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        <Messages />
      </div>

      <ChatInput />
    </div>
  );
}
