import { useState } from "react";

function ChatInput({ onSend }) {

    const [question, setQuestion] = useState("");

    const send = () => {

        if (!question.trim()) return;

        onSend(question);

        setQuestion("");

    };

    return (

        <div
            style={{
                display: "flex",
                padding: "16px 20px",
                gap: 10,
                borderTop: "1px solid #e5e7eb",
                background: "rgba(255,255,255,0.95)",
                backdropFilter: "blur(10px)"
            }}
        >

            <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") send();
                }}
                placeholder="Ask about revenue, customers..."
                style={{
                    flex: 1,
                    padding: "14px 16px",
                    fontSize: 15,
                    borderRadius: 999,
                    border: "1px solid #dbe4f0",
                    outline: "none",
                    boxShadow: "inset 0 1px 2px rgba(15, 23, 42, 0.04)"
                }}
            />

            <button
                onClick={send}
                style={{
                    background: "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                    color: "white",
                    border: "none",
                    padding: "14px 20px",
                    borderRadius: 999,
                    cursor: "pointer",
                    fontWeight: 600,
                    boxShadow: "0 8px 20px rgba(37, 99, 235, 0.25)"
                }}
            >
                Send
            </button>

        </div>

    );

}

export default ChatInput;