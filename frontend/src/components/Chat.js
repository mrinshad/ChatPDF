import React, { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const Chat = () => {
  const { documentId } = useParams();
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const chatContainerRef = useRef(null);

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    const newMessage = { question, response: "" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    try {
      const result = await axios.post("/ask", {
        document_id: documentId,
        query: question,
      });

      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        updatedMessages[updatedMessages.length - 1].response =
          result.data.response;
        return updatedMessages;
      });
      setQuestion("");
    } catch (error) {
      console.error("Error asking question:", error);
    }
  };

  // Scroll to the bottom of the chat container whenever messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="container mt-5">
      <h2>Chat with Document: {documentId}</h2>
      {messages.length > 0 && (
        <div
          ref={chatContainerRef}
          className="chat-container"
          style={{
            maxHeight: "400px",
            overflowY: "scroll",
            border: "1px solid #ccc",
            padding: "10px",
            borderRadius: "5px",
            marginBottom: "1rem", // Space for the form
          }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className="message"
              style={{ marginBottom: "15px" }}
            >
              <div
                className="question"
                style={{ fontWeight: "bold", color: "#007bff" }}
              >
                <strong>Q:</strong> {msg.question}
              </div>
              {msg.response && (
                <div className="answer" style={{ marginTop: "5px" }}>
                  <strong>A:</strong> {msg.response}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      <form onSubmit={handleAskQuestion} className="mt-3">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="form-control"
          placeholder="Ask a question..."
          required
        />
        <button type="submit" className="btn btn-primary mt-2">
          Ask
        </button>
      </form>
    </div>
  );
};

export default Chat;
