import Message from "./Message";

function ChatWindow() {

    const messages = [

        {
            sender:"bot",
            text:"Hello! Ask me anything about revenue, customers, products or channels."
        },

        {
            sender:"user",
            text:"Which channel generated the highest revenue?"
        },

        {
            sender:"bot",
            text:"Paid Search generated $126,170.\n\nSnapshot Used: 2026-07-02"
        }

    ];

    return (

        <div
            style={{
                flex:1,
                overflowY:"auto",
                padding:25
            }}
        >

            {
                messages.map((m,index)=>

                    <Message
                        key={index}
                        sender={m.sender}
                        text={m.text}
                    />

                )
            }

        </div>

    );

}

export default ChatWindow;