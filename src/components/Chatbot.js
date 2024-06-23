import React, { useState } from 'react';
import axios from 'axios';
import './Chatbot.css';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState('');
    const [isOpen, setIsOpen] = useState(false);

  const sendMessage = async () => {
    const userMessage = { text: userInput, sender: 'user' };
    setMessages([...messages, userMessage]);

    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-4', // Specify the model
          messages: [
            {
              role: "system",
              content: "You are a fitness guide app , for the given request about fitness you should give what excersises should you do in point wise manner and only explain if specified for any other topic other than health and fitness return please ask related to fitness only"
            },
            ...messages.map(msg => ({ role: msg.sender === 'user' ? 'user' : 'assistant', content: msg.text })),
            { role: 'user', content: userInput }
          ],
        },
        {
          headers: {
            'Authorization': `Bearer openai api key`
          }
        }
      );

      const botMessage = { text: response.data.choices[0].message.content, sender: 'bot' };
      setMessages([...messages, userMessage, botMessage]);
      setUserInput('');
    } catch (error) {
      console.error('Failed to send message: ', error);
    }
  };
  if (!isOpen) {
    return (
      <button className="chatbot-toggle" onClick={() => setIsOpen(true)}>
        Chat
      </button>
    );
  }
  return (
        <div className="chatbot-container">
          <button className="chat-close" onClick={() => setIsOpen(false)}>X</button> {/* Close button */}
          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={index} className={`chat-message ${message.sender}`}>
                <p>{message.text}</p>
              </div>
            ))}
          </div>
          <div className="chat-input-container">
            <input
              className="chat-input"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' ? sendMessage() : null}
              maxLength="40" // Limit input length
            />
            <button className="chat-send" onClick={sendMessage}>Send</button>
          </div>
        </div>
      );
    };
    
export default Chatbot;
