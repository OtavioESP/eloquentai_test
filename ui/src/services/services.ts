import api from "./config";

interface ILoginResponse {
  success: boolean;
  message: string;
  user: any;
  chat: string;
}

interface Match {
    id: string
    score: number
    metadata?: object
}

interface IChatResponse {
  query: string;
  matches?: Match[];
  error?: Record<string, any>;
}

export async function makeLogin(username: string, password: string): Promise<ILoginResponse> {
  try {
    const response = await api.post<ILoginResponse>("/users/login", {
      username,
      password,
    });

    if (response.data.user.id) {
      localStorage.setItem("uuid", response.data.user.id);
    }

    return response.data;

  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
}

export async function unloggedEntry(): Promise<ILoginResponse> {
  try {
    const response = await api.post<ILoginResponse>("/users/unlogged");

    if (response.data.user.id) {
      localStorage.setItem("uuid", response.data.user.id);
    }

    return response.data;

  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
}

export async function sendMessage(chatUUID: string, message: string): Promise<string> {
  try {
    const response = await api.post<IChatResponse>("/chat/send/message", {
      chatUUID, message
    });

    if (response.data.matches) {
      return response.data.query;   
    }

    return "Failed attemp, please try again!"

  } catch (error) {
    console.error("Failed attempt, please try again:", error);
    throw error;
  }
}