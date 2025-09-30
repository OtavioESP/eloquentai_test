import React, { useState, useRef, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./Chat.css";
import { sendMessage } from "../services/services";

interface Message {
  id: string;
  role: "user" | "bot";
  content: string;
}

const Chat = () => {
  const [userUUID, setUserUUID] = useState<string>("");
  const [chatUUID, setChatUUID] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const { useruuid, chatuuid } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (useruuid) setUserUUID(useruuid);
    if (chatuuid) setChatUUID(chatuuid);
  }, [useruuid, chatuuid]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };

    setMessages((prev) => [...prev, userMessage]);

    setInput("");

    try {
      // Ads based on response: bot, 
      // not a response: from the user itself
      const data = await sendMessage(chatUUID, content)

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "bot",
        content: data || "No response",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: "bot",
        content: "Failed to send message",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(input);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("uuid");
    navigate("/login", { replace: true });
  };

  return (
    <div className="home-container">
      <aside className="chat-list">
        <h2>EloQ RAG Chat</h2>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </aside>

      <main className="chat-panel">
        <div className="chat-messages-wrapper">
          <div className="chat-messages">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`chat-message ${msg.role === "user" ? "user" : "bot"}`}
              >
                {msg.content}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
            />
            <button onClick={() => handleSendMessage(input)}>Send</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Chat;
