import api from "./config";

interface ILoginResponse {
  success: boolean;
  message: string;
  user: any;
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
