import Message from "./Message";

function ChatWindow({ messages }) {

    return (

        <div
            style={{
                flex: 1,
                overflowY: "auto",
                padding: 25
            }}
        >

            {
                messages.map((msg, index) => (

                    <Message
                        key={index}
                        sender={msg.sender}
                        text={msg.text}
                    />

                ))
            }

        </div>

    );

}

export default ChatWindow;