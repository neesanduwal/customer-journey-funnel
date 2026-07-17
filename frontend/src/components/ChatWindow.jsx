import Message from "./Message";

function ChatWindow({ messages }) {

    return (

        <div
            style={{
                flex: 1,
                overflowY: "auto",
                padding: "24px 20px",
                background: "transparent"
            }}
        >

            {messages.map((message, index) => (

                <Message
                    key={index}
                    sender={message.sender}
                    text={message.text}
                />

            ))}

        </div>

    );

}

export default ChatWindow;