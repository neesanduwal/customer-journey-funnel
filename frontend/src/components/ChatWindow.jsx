import Message from "./Message";

function ChatWindow({ messages }) {

    return (

        <div
            style={{
                flex: 1,
                overflowY: "auto",
                padding: 20,
                background: "#f5f5f5"
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