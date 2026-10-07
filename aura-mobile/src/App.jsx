import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("aura_token") || "");
  const [authMode, setAuthMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) {
      localStorage.setItem("aura_token", token);
    } else {
      localStorage.removeItem("aura_token");
    }
  }, [token]);

  const register = async () => {
    const userEmail = email.trim();

    if (!userEmail || !password) {
      setAuthError("Email aur password enter karo.");
      return;
    }

    if (password.length < 10) {
      setAuthError("Password kam se kam 10 characters ka hona chahiye.");
      return;
    }

    setAuthLoading(true);
    setAuthError("");

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: userEmail,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      setAuthMode("login");
      setPassword("");
      setAuthError("Account create ho gaya. Ab login karo.");
    } catch (error) {
      setAuthError(error.message);
    } finally {
      setAuthLoading(false);
    }
  };

  const login = async () => {
    const userEmail = email.trim();

    if (!userEmail || !password) {
      setAuthError("Email aur password enter karo.");
      return;
    }

    setAuthLoading(true);
    setAuthError("");

    try {
      const formData = new URLSearchParams();

      formData.append("username", userEmail);
      formData.append("password", password);

      const response = await fetch("/api/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      setToken(data.access_token);
      setPassword("");
      setAuthError("");
    } catch (error) {
      setAuthError(error.message);
    } finally {
      setAuthLoading(false);
    }
  };

  const logout = () => {
    setToken("");
    setMessages([]);
    setMessage("");
  };

  const sendMessage = async () => {
    const text = message.trim();

    if (!text || loading || !token) return;

    setMessages((old) => [...old, { role: "user", text }]);
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      const data = await response.json();

      if (response.status === 401) {
        logout();
        throw new Error("Session expire ho gayi. Dobara login karo.");
      }

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

  if (!token) {
    return (
      <div className="app">
        <div className="auth-card">
          <div className="logo auth-logo">A</div>

          <h1>AURA</h1>
          <span className="auth-subtitle">AI Assistant</span>

          <h2>
            {authMode === "login" ? "Welcome back" : "Create your AURA account"}
          </h2>

          <p className="auth-description">
            {authMode === "login"
              ? "Login karke AURA se baat karein."
              : "AURA use karne ke liye account banayein."}
          </p>

          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            disabled={authLoading}
          />

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            disabled={authLoading}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                authMode === "login" ? login() : register();
              }
            }}
          />

          {authError && <div className="auth-message">{authError}</div>}

          <button
            className="auth-button"
            onClick={authMode === "login" ? login : register}
            disabled={authLoading}
          >
            {authLoading
              ? "Please wait..."
              : authMode === "login"
              ? "Login"
              : "Create Account"}
          </button>

          <button
            className="switch-auth"
            onClick={() => {
              setAuthError("");
              setAuthMode(authMode === "login" ? "register" : "login");
            }}
            disabled={authLoading}
          >
            {authMode === "login"
              ? "New user? Create account"
              : "Already have an account? Login"}
          </button>

          <div className="bottom-text">
            AURA AI • Local + Online Intelligence
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">A</div>

        <div>
          <h1>AURA</h1>
          <span>AI Assistant</span>
        </div>

        <div className="header-actions">
          <div className="status">●</div>

          <button className="logout" onClick={logout}>
            Logout
          </button>
        </div>
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