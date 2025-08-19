import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import DataTable from './components/DataTable';

function App() {
  const [currentResponse, setCurrentResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleNewResponse = (response) => {
    setCurrentResponse(response);
    setIsLoading(false);
  };

  const handleLoadingStart = () => {
    setIsLoading(true);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Sewer AI - Infrastructure Analysis</h1>
        <p>AI-powered analysis of municipal sewer inspection data</p>
      </header>
      
      <div className="main-content">
        <div className="chat-panel">
          <ChatInterface 
            onNewResponse={handleNewResponse}
            onLoadingStart={handleLoadingStart}
            isLoading={isLoading}
          />
        </div>
        
        <div className="results-panel">
          {isLoading && (
            <div className="loading">
              <h3>Analyzing data...</h3>
              <div className="spinner"></div>
            </div>
          )}
          
          {currentResponse && !isLoading && (
            <div className="results">
              <div className="ai-response">
                <h3>Analysis</h3>
                <div className="response-text">
                  {currentResponse.response}
                </div>
              </div>
              
              {currentResponse.table_data && (
                <DataTable data={currentResponse.table_data} />
              )}
            </div>
          )}
          
          {!currentResponse && !isLoading && (
            <div className="empty-state">
              <h3>Ask a question to see analysis</h3>
              <p>Try: "What cities have the most inspections?"</p>
              <div className="sample-queries">
                <h4>Sample Questions:</h4>
                <ul>
                  <li>What kind of inspection projects are in this data?</li>
                  <li>Show me emergency inspections by city</li>
                  <li>Which cities should we prioritize for investment?</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;