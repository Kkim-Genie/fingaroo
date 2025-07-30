export interface ChatApiRequest {
  query: string;
  thread_id?: string;
}

export interface InterruptRequest {
  payload: { result: string };
  thread_id: string;
}

const API_PATH = process.env.NEXT_PUBLIC_API_PATH || "http://localhost:8000";

export class ChatApiService {
  static async sendFirstChat(request: ChatApiRequest): Promise<Response> {
    const response = await fetch(`${API_PATH}/chat/first`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: request.query,
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

    const response = await fetch(`${API_PATH}/chat/continue`, {
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
    const response = await fetch(`${API_PATH}/chat/interrupt`, {
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
