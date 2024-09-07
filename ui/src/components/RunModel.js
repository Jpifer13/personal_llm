import React, { useState, useEffect, useRef } from 'react';

function RunModel() {
  const [prompt, setPrompt] = useState('');
  const [responses, setResponses] = useState([]);
  const [typingResponse, setTypingResponse] = useState('');

  const responseContainerRef = useRef(null);

  useEffect(() => {
    if (responseContainerRef.current) {
      responseContainerRef.current.scrollTop = responseContainerRef.current.scrollHeight;
    }
  }, [typingResponse, responses]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/run`);

    let currentResponse = '';
    ws.onopen = () => {
      ws.send(prompt);
    };

    ws.onmessage = (event) => {
      currentResponse += event.data;
      setTypingResponse(currentResponse);
    };

    ws.onclose = () => {
      setResponses((prevResponses) => [
        ...prevResponses,
        currentResponse,
      ]);
      setTypingResponse('');
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
      <div id="results" ref={responseContainerRef}>
        {responses.map((response, index) => (
          <div key={index} className="result">
            <h2>Generated Text {index + 1}:</h2>
            <textarea value={response} rows="10" readOnly />
          </div>
        ))}
        {typingResponse && (
          <div className="result">
            <h2>Typing...</h2>
            <textarea value={typingResponse} rows="10" readOnly />
          </div>
        )}
      </div>
    </div>
  );
}

export default RunModel;
