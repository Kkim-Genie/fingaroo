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
  handleSubmit: (
    e: React.FormEvent<HTMLFormElement>,
    directInput?: string
  ) => void;
  setInput: (input: string) => void;
}

export interface User {
  id: string;
  name: string;
  email: string;
  gender: string;
  birthyear: number;
}

export interface InvestLog {
  id: string;
  user_id: string;
  date: string;
  stock_code: string;
  stock_name: string;
  action: string;
  price: number;
  amount: number;
  reason: string;
  amount_ratio: number;
  profit: number;
  profit_ratio: number;
  created_at: string;
}

export interface CreateInvestLogRequest {
  date: string;
  stock_code: string;
  stock_name: string;
  action: string;
  price: number;
  amount: number;
  reason: string;
  amount_ratio: number;
  profit: number;
  profit_ratio: number;
}

export interface UpdateInvestLogRequest {
  invest_log: InvestLog;
}

export interface UserAsset {
  id: string;
  user_id: string;
  stock_code: string;
  stock_name: string;
  amount: number;
}

export interface CreateUserAssetRequest {
  stock_code: string;
  stock_name: string;
  amount: number;
}

export interface UpdateUserAssetRequest {
  user_asset: UserAsset;
}
