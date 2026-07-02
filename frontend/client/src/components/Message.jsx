function Message({ sender, text }) {

    const isUser = sender === "user";

    return (

        <div
            style={{
                display:"flex",
                justifyContent:isUser ? "flex-end":"flex-start",
                marginBottom:15
            }}
        >

            <div
                style={{
                    background:isUser ? "#2563EB":"white",
                    color:isUser ? "white":"black",
                    padding:15,
                    borderRadius:12,
                    maxWidth:"70%",
                    boxShadow:"0 2px 8px rgba(0,0,0,0.1)"
                }}
            >
                {text}
            </div>

        </div>

    );

}

export default Message;