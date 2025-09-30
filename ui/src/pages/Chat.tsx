import React, { useState, useRef, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./Chat.css";

interface Message {
    id: string;
    role: "user" | "bot";
    content: string;
}

interface Chat {
    id: string;
    name: string;
    messages: Message[];
}

const mockChats: Chat[] = [
    { id: "1", name: "Chat 1", messages: [] },
    { id: "2", name: "Chat 2", messages: [] },
];

const Chat = () => {
    const [userUUID, setUserUUID] = useState<string>("");
    const [chats, setChats] = useState<Chat[]>(mockChats);
    const [selectedChatId, setSelectedChatId] = useState<string>("1");
    const [input, setInput] = useState("");
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    const { uuid } = useParams();
    const navigate = useNavigate();

    const selectedChat = chats.find((c) => c.id === selectedChatId);

    useEffect(() => {

        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [selectedChat?.messages]);

    useEffect(() => {
        if (uuid !== undefined && uuid != null)
            setUserUUID(uuid);

    }, [])

    const handleSend = () => {
        if (!input.trim() || !selectedChat) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: "user",
            content: input,
        };

        const botMessage: Message = {
            id: (Date.now() + 1).toString(),
            role: "bot",
            content: `Echo: ${input}`,
        };

        setChats((prev) =>
            prev.map((chat) =>
                chat.id === selectedChatId
                    ? { ...chat, messages: [...chat.messages, userMessage, botMessage] }
                    : chat
            )
        );

        setInput("");
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleLogout = () => {
        // Clear the stored UUID from localStorage
        localStorage.removeItem("uuid");
        // Navigate back to login page
        navigate("/login", { replace: true });
    };

    return (
        <div className="home-container">
            <aside className="chat-list">
                <h2>Chats</h2>
                <ul>
                    {chats.map((chat) => (
                        <li
                            key={chat.id}
                            className={chat.id === selectedChatId ? "active" : ""}
                            onClick={() => setSelectedChatId(chat.id)}
                        >
                            {chat.name}
                        </li>
                    ))}
                </ul>
                <button className="logout-button" onClick={handleLogout}>
                    Logout
                </button>
            </aside>

            <main className="chat-panel">
                <div className="chat-messages-wrapper">
                    <div className="chat-messages">
                        {selectedChat?.messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={`chat-message ${msg.role === "user" ? "user" : "bot"
                                    }`}
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
                        <button onClick={handleSend}>Send</button>
                    </div>
                </div>
            </main>
        </div>

    );
};

export default Chat;
