function Message({ sender, text }) {

    const isUser = sender === "user";

    return (
        <div
            style={{
                display: "flex",
                justifyContent: isUser ? "flex-end" : "flex-start",
                marginBottom: 14
            }}
        >
            <div
                style={{
                    background: isUser ? "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)" : "#ffffff",
                    color: isUser ? "white" : "#111827",
                    padding: "12px 16px",
                    borderRadius: isUser ? "18px 18px 6px 18px" : "18px 18px 18px 6px",
                    maxWidth: "76%",
                    whiteSpace: "pre-wrap",
                    boxShadow: "0 10px 25px rgba(15, 23, 42, 0.08)",
                    border: isUser ? "none" : "1px solid #e2e8f0"
                }}
            >
                {text}
            </div>
        </div>
    );
}

export default Message;