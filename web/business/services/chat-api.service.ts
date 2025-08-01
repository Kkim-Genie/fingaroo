import { API_URL } from "@/utils/consts";

export interface FirstChatApiRequest {
  query: string;
  access_token: string;
  refresh_token: string;
}

export interface ChatApiRequest {
  query: string;
  thread_id?: string;
}

export interface InterruptRequest {
  payload: { result: string };
  thread_id: string;
}

export class ChatApiService {
  static async sendFirstChat(request: FirstChatApiRequest): Promise<Response> {
    const response = await fetch(`${API_URL}/chat/first`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: request.query,
        access_token: request.access_token,
        refresh_token: request.refresh_token,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  }

  static async sendContinueChat(request: ChatApiRequest): Promise<Response> {
    if (!request.thread_id) {
      throw new Error("Thread ID is required for continue chat");
    }

    const response = await fetch(`${API_URL}/chat/continue`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: request.query,
        thread_id: request.thread_id,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  }

  static async sendInterrupt(request: InterruptRequest): Promise<Response> {
    const response = await fetch(`${API_URL}/chat/interrupt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        payload: request.payload,
        thread_id: request.thread_id,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  }
}
