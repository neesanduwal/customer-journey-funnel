import { useState } from "react";

import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import api from "../services/api";

function ChatPage() {

    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hello! Ask me about revenue, leads, customers or products."
        }
    ]);

    const sendQuestion = async (question) => {

        setMessages(prev => [
            ...prev,
            {
                sender: "user",
                text: question
            }
        ]);

        try {

            const response = await api.post("/chat", {
                question: question
            });

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: response.data.answer
                }
            ]);

        }
        catch {

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: "Unable to contact backend."
                }
            ]);

        }

    };

    return (

        <div
            style={{
                display: "flex",
                flexDirection: "column",
                height: "100vh"
            }}
        >

            <Header />

            <ChatWindow messages={messages} />

            <ChatInput onSend={sendQuestion} />

        </div>

    );

}

export default ChatPage;