import { useState, useRef, useEffect } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<{ role: string; text: string }[]>(() => {
    const saved = localStorage.getItem("chat");
    return saved ? JSON.parse(saved) : [];
  });
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    localStorage.setItem("chat", JSON.stringify(messages));
  }, [messages]);

  const newChat = () => {
    setMessages([]);
    setMessage("");
    localStorage.removeItem("chat");
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const currentMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: currentMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: currentMessage }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: data.response,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        background: "#000",
        color: "#00ff6a",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
        fontFamily: "-apple-system, BlinkMacSystemFont, sans-serif",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1400px",
          height: "92vh",
          background: "rgba(0,0,0,0.85)",
          borderRadius: "32px",
          overflow: "hidden",
          boxShadow: "0 20px 60px rgba(0,255,106,0.15)",
          display: "flex",
        }}
      >
        <div
          style={{
            width: "280px",
            padding: "24px",
            borderRight: "1px solid rgba(0,255,106,0.15)",
            background: "rgba(0,0,0,0.9)",
            display: "flex",
            flexDirection: "column",
            gap: "20px",
          }}
        >
          <div>
            <h1
              style={{
                margin: 0,
                fontSize: "28px",
                fontWeight: 700,
                color: "#00ff6a",
              }}
            >
              AI Agent Hub
            </h1>
            <p
              style={{
                color: "#9cff9e",
              }}
            >
              Gemini • LangGraph
            </p>
          </div>

          <button
            onClick={newChat}
            style={{
              padding: "14px",
              borderRadius: "16px",
              border: "none",
              background: "#00ff6a",
              color: "#000",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            + New Chat
          </button>
        </div>

        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            background: "rgba(0,0,0,0.45)",
            backdropFilter: "blur(20px)",
            borderLeft: "1px solid rgba(0,255,106,0.15)",
          }}
        >
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              padding: "30px",
            }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
                  marginBottom: "16px",
                }}
              >
                <div
                  style={{
                    maxWidth: "70%",
                    padding: "14px 18px",
                    borderRadius: "24px",
                    whiteSpace: "pre-wrap",
                    background: msg.role === "user" ? "rgba(0,255,106,0.15)" : "rgba(255,255,255,0.08)",
                    color: msg.role === "user" ? "#b8ffb7" : "#e5ffdb",
                    border: msg.role === "user" ? "1px solid rgba(0,255,106,0.4)" : "1px solid rgba(255,255,255,0.12)",
                    boxShadow: "0 8px 30px rgba(0,0,0,0.15)",
                  }}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {loading && (
              <div
                style={{
                  padding: "14px 18px",
                  background: "rgba(255,255,255,0.08)",
                  borderRadius: "24px",
                  width: "fit-content",
                  color: "#b8ffb7",
                  border: "1px solid rgba(255,255,255,0.12)",
                  boxShadow: "0 8px 30px rgba(0,0,0,0.12)",
                }}
              >
                Thinking...
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div
            style={{
              padding: "20px",
              borderTop: "1px solid rgba(0,255,106,0.15)",
              display: "flex",
              gap: "12px",
            }}
          >
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
              placeholder="Ask anything..."
              style={{
                flex: 1,
                padding: "16px",
                borderRadius: "18px",
                border: "1px solid rgba(0,255,106,0.3)",
                outline: "none",
                background: "rgba(0,0,0,0.7)",
                color: "#b8ffb7",
                fontSize: "16px",
              }}
            />

            <button
              disabled={loading}
              onClick={sendMessage}
              style={{
                width: "60px",
                height: "60px",
                borderRadius: "50%",
                border: "none",
                background: "#00ff6a",
                color: "#000",
                cursor: "pointer",
                fontSize: "18px",
              }}
            >
              {loading ? "..." : "➜"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
