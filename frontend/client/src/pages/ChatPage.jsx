import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

function ChatPage() {

    return (

        <div
            style={{
                display:"flex",
                flexDirection:"column",
                height:"100vh"
            }}
        >

            <Header/>

            <ChatWindow/>

            <ChatInput/>

        </div>

    );

}

export default ChatPage;