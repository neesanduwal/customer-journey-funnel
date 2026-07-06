import { useState } from "react";

import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import API from "../services/api";

function ChatPage() {

    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hello! Ask me anything about your customer journey data."
        }
    ]);

    async function sendQuestion(question) {

        setMessages(prev => [
            ...prev,
            {
                sender: "user",
                text: question
            }
        ]);

        try {

            const response = await API.post("/chat", {
                question
            });

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: response.data.answer
                }
            ]);

        } catch (err) {

            console.error(err);

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: "Unable to contact backend."
                }
            ]);

        }

    }

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