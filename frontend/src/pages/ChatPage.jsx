import { useState } from "react";

import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import api from "../services/api";

function ChatPage() {

    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hello! Ask me about your customer journey."
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
                question
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
                    text: "Backend is not running."
                }
            ]);

        }

    };

    return (

        <div style={{
            display: "flex",
            flexDirection: "column",
            height: "100vh"
        }}>

            <Header />

            <ChatWindow messages={messages} />

            <ChatInput onSend={sendQuestion} />

        </div>

    );

}

export default ChatPage;