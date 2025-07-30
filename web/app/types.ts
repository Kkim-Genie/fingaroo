export interface BaseMessage {
  type: "system" | "human" | "ai" | "tool" | "tool_call";
  content: string;
  id: string;
}

export interface UsageMetadata {
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
}

export interface HumanMessage extends BaseMessage {
  type: "human";
}

export interface AiMessage extends BaseMessage {
  type: "ai";
  usage_metadata: UsageMetadata;
  name: string;
}

export interface SystemMessage extends BaseMessage {
  type: "system";
}

export interface ToolMessage extends BaseMessage {
  type: "tool";
  tool_name: string;
  tool_call_id: string;
}

export interface ToolCallMessage extends BaseMessage {
  type: "tool_call";
  tool_name: string;
  usage_metadata: UsageMetadata;
  arguments: Record<string, unknown>;
}

export interface ChatProviderProps {
  messages: BaseMessage[];
  isLoading: boolean;
  input: string;
  handleInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  setInput: (input: string) => void;
}

export interface User {
  id: string;
  name: string;
  email: string;
  gender: string;
  birthyear: number;
}
