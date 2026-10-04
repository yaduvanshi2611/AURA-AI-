import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const text = message.trim();
    if (!text || loading) return;

    setMessages((old) => [...old, { role: "user", text }]);
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "AURA server error");
      }

      setMessages((old) => [
        ...old,
        {
          role: "aura",
          text: data.reply || "AURA se response nahi mila.",
        },
      ]);
    } catch (error) {
      setMessages((old) => [
        ...old,
        {
          role: "aura",
          text: "AURA connection error: " + error.message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">A</div>
        <div>
          <h1>AURA</h1>
          <span>AI Assistant</span>
        </div>
        <div className="status">●</div>
      </header>

      <main className="chat">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="aura-icon">✦</div>
            <h2>Namaste 👋</h2>
            <p>
              Main AURA hoon. Aap mujhse kuch bhi pooch sakte hain.
            </p>

            <div className="suggestions">
              <button onClick={() => setMessage("Aaj ka mausam kya hai?")}>
                🌤️ Aaj ka mausam
              </button>

              <button onClick={() => setMessage("Mujhe business idea do")}>
                💡 Business idea
              </button>

              <button onClick={() => setMessage("Mujhe kuch naya sikhao")}>
                🧠 Kuch naya sikhao
              </button>
            </div>
          </div>
        ) : (
          messages.map((item, index) => (
            <div
              key={index}
              className={
                item.role === "user"
                  ? "message user"
                  : "message aura"
              }
            >
              <div className="bubble">{item.text}</div>
            </div>
          ))
        )}

        {loading && (
          <div className="message aura">
            <div className="bubble">AURA soch raha hai...</div>
          </div>
        )}
      </main>

      <div className="input-area">
        <button className="plus">+</button>

        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
          placeholder="Ask AURA..."
          disabled={loading}
        />

        <button
          className="send"
          onClick={sendMessage}
          disabled={loading}
        >
          ↑
        </button>
      </div>

      <div className="bottom-text">
        AURA AI • Local + Online Intelligence
      </div>
    </div>
  );
}

export default App;
