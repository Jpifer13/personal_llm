import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [responses, setResponses] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const ws = new WebSocket(`ws://${window.location.hostname}:8000/ws`);

    let generatedText = '';
    ws.onopen = () => {
      ws.send(prompt);
    };

    ws.onmessage = (event) => {
      generatedText += event.data;
      setResponses((prevResponses) => [
        ...prevResponses.slice(0, -1),
        generatedText,
      ]);
    };

    ws.onclose = () => {
      setResponses((prevResponses) => [...prevResponses, generatedText]);
    };
  };

  return (
    <div className="container">
      <h1>Text Generation with GPT-2</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="prompt">Enter a prompt:</label>
        <textarea
          id="prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows="4"
          required
        />
        <button type="submit">Generate Text</button>
      </form>
      <div id="results">
        {responses.map((response, index) => (
          <div key={index} className="result">
            <h2>Generated Text:</h2>
            <textarea value={response} rows="10" readOnly />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
