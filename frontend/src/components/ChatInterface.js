import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface = ({ onNewResponse, onLoadingStart, isLoading }) => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([
    {
      type: 'bot',
      message: 'Hello! I can help you analyze sewer inspection data. Ask me about cities, inspection types, or specific infrastructure insights.',
      timestamp: new Date()
    }
  ]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim() || isLoading) return;
    
    const userMessage = {
      type: 'user',
      message: query.trim(),
      timestamp: new Date()
    };
    
    setChatHistory(prev => [...prev, userMessage]);
    onLoadingStart();
    
    try {
      const response = await axios.post('http://localhost:5001/api/chat', {
        query: query.trim()
      });
      
      const botMessage = {
        type: 'bot',
        message: response.data.response,
        timestamp: new Date(),
        tableData: response.data.table_data
      };
      
      setChatHistory(prev => [...prev, botMessage]);
      onNewResponse(response.data);
      
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        message: 'Sorry, I encountered an error processing your question. Please try again.',
        timestamp: new Date(),
        isError: true
      };
      
      setChatHistory(prev => [...prev, errorMessage]);
      console.error('Chat error:', error);
    }
    
    setQuery('');
  };

  const handleSampleQuery = (sampleQuery) => {
    setQuery(sampleQuery);
  };

  const sampleQueries = [
    "What cities have the most inspections?",
    "What kind of inspection projects are in this data?",
    "Show me emergency inspections by city",
    "Give me an overview of this data"
  ];

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>Ask Questions</h3>
      </div>
      
      <div className="chat-messages">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-content">
              <div className="message-text">{msg.message}</div>
              <div className="message-time">
                {msg.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot loading-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>
      
      <div className="sample-queries">
        <p>Try these questions:</p>
        {sampleQueries.map((sample, index) => (
          <button 
            key={index}
            className="sample-query-btn"
            onClick={() => handleSampleQuery(sample)}
            disabled={isLoading}
          >
            {sample}
          </button>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about sewer inspection data..."
            className="chat-input"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            disabled={!query.trim() || isLoading}
            className="send-btn"
          >
            {isLoading ? 'Analyzing...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;