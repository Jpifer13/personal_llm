import React, { useState } from 'react';

function FineTune() {
  const [file, setFile] = useState(null);
  const [datasetName, setDatasetName] = useState("");
  const [status, setStatus] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!file || !datasetName) {
      setStatus("Please select a file and enter a dataset name.");
      return;
    }

    const reader = new FileReader();
    reader.onload = async () => {
      const dataset = JSON.parse(reader.result);
      const ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/upload`);

      ws.onopen = () => {
        ws.send(JSON.stringify({ dataset_name: datasetName, dataset }));
      };

      ws.onmessage = (event) => {
        setStatus(event.data);
        if (event.data === "Fine-tuning completed.") {
          setDownloadUrl(`http://${window.location.hostname}:8000/download/${datasetName}`);
        }
      };

      ws.onclose = () => {
        console.log("Connection closed");
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    };

    reader.readAsText(file);
  };

  return (
    <div className="container">
      <h1>Upload Dataset for GPT-2 Fine-Tuning</h1>
      <input 
        type="text" 
        placeholder="Enter dataset name" 
        value={datasetName} 
        onChange={(e) => setDatasetName(e.target.value)} 
      />
      <input type="file" accept=".json" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Fine-Tune</button>
      <p>Status: {status}</p>
      {downloadUrl && (
        <div>
          <a href={downloadUrl} download={`${datasetName}.zip`}>
            Download Fine-Tuned Model
          </a>
        </div>
      )}
    </div>
  );
}

export default FineTune;
