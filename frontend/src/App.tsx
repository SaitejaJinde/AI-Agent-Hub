import { useState, useRef, useEffect } from "react";
function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<
    { role: string; text: string }[]
  >(() => {
    const saved = localStorage.getItem("chat");

    return saved ? JSON.parse(saved) : [];
  });
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  useEffect(() => {
    localStorage.setItem(
      "chat",
      JSON.stringify(messages)
    );
  }, [messages]);

  const newChat = () => {
    setMessages([]);
    setMessage("");
    localStorage.removeItem("chat");
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const currentMessage = message;

    const userMessage = {
      role: "user",
      text: currentMessage,
    };

    setMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: currentMessage,
        }),
      });

      const data = await res.json();

      const aiMessage = {
        role: "ai",
        text: data.response,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
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
        maxWidth: "1000px",
        margin: "0 auto",
        padding: "20px",
        fontFamily: "Arial, sans-serif",
        display: "flex",
        gap: "20px",
      }}
    >
      {/* Sidebar */}
      <div
        style={{
          width: "250px",
          padding: "20px",
          borderRadius: "12px",
          backgroundColor: "#f7f7f7",
          border: "1px solid #ddd",
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        <div style={{ fontSize: "24px", fontWeight: "700" }}>
          🤖 AI Agent Hub
        </div>
        <button
          onClick={newChat}
          style={{
            padding: "12px 16px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#2563eb",
            color: "white",
            cursor: "pointer",
          }}
        >
          + New Chat
        </button>
      </div>

      {/* Main Chat */}
      <div style={{ flex: 1 }}>
        <div
          style={{
            minHeight: "500px",
            border: "1px solid #ddd",
            borderRadius: "12px",
            backgroundColor: "#fafafa",
            padding: "20px",
            marginBottom: "20px",
            overflowY: "auto",
          }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                justifyContent:
                  msg.role === "user"
                    ? "flex-end"
                    : "flex-start",
                marginBottom: "15px",
              }}
            >
              <div
                style={{
                  maxWidth: "70%",
                  padding: "12px",
                  borderRadius: "12px",
                  backgroundColor:
                    msg.role === "user"
                      ? "#2563eb"
                      : "#e5e7eb",
                  color:
                    msg.role === "user"
                      ? "white"
                      : "black",
                  whiteSpace: "pre-wrap",
                }}
              >
                {msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div
              style={{
                display: "flex",
                justifyContent: "flex-start",
                marginBottom: "15px",
              }}
            >
              <div
                style={{
                  backgroundColor: "#e5e7eb",
                  padding: "12px",
                  borderRadius: "12px",
                }}
              >
                Thinking...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          <input
            style={{
              flex: 1,
              padding: "12px",
              borderRadius: "8px",
              border: "1px solid #ccc",
            }}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask anything..."
          />

          <button
            disabled={loading}
            onClick={sendMessage}
            style={{
              padding: "12px 24px",
              borderRadius: "8px",
              border: "none",
              backgroundColor: "#2563eb",
              color: "white",
              cursor: "pointer",
            }}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;