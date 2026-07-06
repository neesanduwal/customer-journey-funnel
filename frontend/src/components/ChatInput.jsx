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
                padding: 15,
                gap: 10,
                borderTop: "1px solid #ddd",
                background: "white"
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
                    padding: 14,
                    fontSize: 16,
                    borderRadius: 8,
                    border: "1px solid #ccc"
                }}
            />

            <button
                onClick={send}
                style={{
                    background: "#2563eb",
                    color: "white",
                    border: "none",
                    padding: "14px 22px",
                    borderRadius: 8,
                    cursor: "pointer"
                }}
            >
                Send
            </button>

        </div>

    );

}

export default ChatInput;