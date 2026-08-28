import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { sendChatMessage } from "../services/api";

const ChatInterface = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const submit = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;
    const userMessage = message;
    setMessage("");
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    try {
      const response = await sendChatMessage(userMessage);
      setMessages((prev) => [...prev, { role: "assistant", text: response.response }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "assistant", text: "Error contacting RAGHUVIR API." }]);
    }
  };

  return (
    <section className="card">
      <h2>Chat</h2>
      <button type="button">🎤 Voice (Phase 5)</button>
      <div className="messages">
        {messages.map((m, index) => (
          <div key={`${m.role}-${index}`} className={`msg ${m.role}`}>
            <strong>{m.role}:</strong> <ReactMarkdown>{m.text}</ReactMarkdown>
          </div>
        ))}
      </div>
      <form onSubmit={submit}>
        <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Hey RAGHUVIR..." />
        <button type="submit">Send</button>
      </form>
    </section>
  );
};

export default ChatInterface;
