import React, { useState, useEffect } from 'react';
import { ChatService } from '../../Service/ChatService';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Chatbot.css';

function Chatbot() {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [chatHistory, setChatHistory] = useState([
    { sender: 'bot', text: 'Welcome to the Financial Advisor Chatbot! How can I assist you today?', timestamp: new Date() },
  ]);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onresult = (event) => {
        setMessage(event.results[0][0].transcript);
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognitionInstance);
    } else {
      console.error('Speech Recognition not supported by this browser.');
    }
  }, []);

  const sendMessage = async () => {
    const botResponse = await ChatService(message);
    const timestamp = new Date();

    setChatHistory((prev) => [
      ...prev,
      { sender: 'user', text: message, timestamp },
      { sender: 'bot', text: formatResponse(botResponse), timestamp },
    ]);

    speakResponse(botResponse);
    setMessage('');
  };

  const formatResponse = (text) => {
    const points = text.split('.').filter(point => point.trim() !== '').map(point => `• ${point.trim()}.`);
    return points.join('\n');
  };

  const speakResponse = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      window.speechSynthesis.speak(utterance);
    } else {
      console.error('Speech Synthesis not supported by this browser.');
    }
  };

  const startListening = () => {
    if (recognition && !isListening) {
      setIsListening(true);
      recognition.start();
    }
  };

  const formatTimestamp = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chatbot-container container-fluid d-flex flex-column justify-content-between">
      <h1 className="text-center fw-bold text-danger">Finance 41</h1>
      <div className="chat-history mb-3 overflow-auto" style={{ flexGrow: 1 }}>
        {chatHistory.map((chat, index) => (
          <div key={index} className={`chat-message ${chat.sender}`}>
            <div className={`message-bubble ${chat.sender}`}>
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'Open Sans,Arial ,sans-serif', fontSize:'16px' }}>{chat.text}</pre>
              <span   style={{ whiteSpace: 'pre-wrap', fontFamily: 'Open Sans,Arial ,sans-serif', fontSize:'12px' }} className="timestamp">{formatTimestamp(chat.timestamp)}</span>
            </div>
          </div>
        ))}
      </div>
      <div className="input-area d-flex align-items-center">
        <input 
          type="text" 
          className="form-control me-2" 
          value={message} 
          onChange={(e) => setMessage(e.target.value)} 
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()} 
          placeholder="Ask for financial advice..." 
        />
        <button className="btn btn-primary" onClick={sendMessage}>Send</button>
        <button className="btn btn-secondary ms-2" onClick={startListening}>
          {isListening ? 'Listening...' : <i className="bi bi-mic"></i>}
        </button>
      </div>
    </div>
  );
}

export default Chatbot;