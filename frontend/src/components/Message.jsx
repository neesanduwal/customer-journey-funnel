function Message({ sender, text }) {

    const isUser = sender === "user";

    return (
        <div
            style={{
                display: "flex",
                justifyContent: isUser ? "flex-end" : "flex-start",
                marginBottom: 12
            }}
        >
            <div
                style={{
                    background: isUser ? "#2563eb" : "#e5e7eb",
                    color: isUser ? "white" : "#111827",
                    padding: "12px 16px",
                    borderRadius: "18px",
                    maxWidth: "70%",
                    whiteSpace: "pre-wrap"
                }}
            >
                {text}
            </div>
        </div>
    );
}

export default Message;