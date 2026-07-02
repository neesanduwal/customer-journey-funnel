function ChatInput() {

    return (

        <div
            style={{
                display:"flex",
                padding:20,
                borderTop:"1px solid #ddd",
                background:"white"
            }}
        >

            <input

                type="text"
                placeholder="Ask about revenue, orders, leads..."

                style={{
                    flex:1,
                    padding:12,
                    borderRadius:8,
                    border:"1px solid #ccc",
                    fontSize:16
                }}

            />

            <button

                style={{
                    marginLeft:10,
                    padding:"12px 24px",
                    background:"#2563EB",
                    color:"white",
                    border:"none",
                    borderRadius:8
                }}

            >
                Send
            </button>

        </div>

    );

}

export default ChatInput;