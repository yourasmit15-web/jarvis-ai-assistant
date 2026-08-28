import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { sendChat } from "../services/api";

export default function ChatInterface() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;

    const userMessage = { role: "user", message };
    setMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setError("");

    try {
      const { data } = await sendChat(userMessage.message);
      setMessages((prev) => [...prev, { role: "assistant", message: data.response }]);
    } catch (err) {
      setError(err.response?.data?.detail || "Request failed");
    }
  };

  return (
    <section className="card">
      <h2>Chat Interface</h2>
      <button type="button" className="voice-btn">🎤 Voice (Phase 5)</button>
      <div className="chat-log">
        {messages.map((item, index) => (
          <article key={index} className={`msg ${item.role}`}>
            <strong>{item.role}: </strong>
            <ReactMarkdown>{item.message}</ReactMarkdown>
          </article>
        ))}
      </div>
      {error && <p className="error">{error}</p>}
      <form onSubmit={onSubmit}>
        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask JARVIS..."
          aria-label="message"
        />
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
