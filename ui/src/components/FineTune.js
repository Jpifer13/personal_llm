import React, { useState } from 'react';

function FineTune() {
  const [file, setFile] = useState(null);
  const [datasetName, setDatasetName] = useState("");
  const [status, setStatus] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus("");
  };

  const handleUpload = () => {
    if (!file) {
      setStatus("Please select a file to upload.");
      return;
    }

    // Check if the file is JSON and require dataset name
    const isJson = file.name.endsWith(".json");

    if (isJson) {
      if (!datasetName) {
        setStatus("Please enter a dataset name for the JSON file.");
        return;
      }
      handleJsonUpload();
    } else if (file.name.endsWith(".pdf")) {
      handlePdfUpload();
    } else {
      setStatus("Unsupported file type. Please upload a PDF or JSON file.");
    }
  };

  const handleJsonUpload = () => {
    const ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/upload`);

    ws.onopen = () => {
      const reader = new FileReader();
      reader.onload = () => {
        const fileData = reader.result;

        // Prepare the payload for JSON
        const payload = {
          file_name: file.name,
          file_data: fileData,
          dataset_name: datasetName,
        };

        ws.send(JSON.stringify(payload));
      };
      reader.readAsDataURL(file);
    };

    ws.onmessage = (event) => {
      setStatus(event.data);
      if (event.data === "Fine-tuning completed.") {
        setDownloadUrl(`http://${window.location.hostname}:8000/download/${datasetName}`);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setStatus("Error during WebSocket upload.");
    };
  };

  const handlePdfUpload = () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataset_name", datasetName);

    setStatus("Uploading PDF...");

    fetch(`http://${window.location.hostname}:8000/upload`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        setStatus(data);
        if (data.includes("Fine-tuning completed")) {
          setDownloadUrl(`http://${window.location.hostname}:8000/download/${file.name}`);
        }
      })
      .catch((error) => {
        console.error("Error during PDF upload:", error);
        setStatus("Error during PDF upload.");
      });
  };

  return (
    <div className="container">
      <h1>Upload Dataset or PDF for GPT-2 Fine-Tuning</h1>
      <input
        type="text"
        placeholder="Enter dataset name (required for JSON)"
        value={datasetName}
        onChange={(e) => setDatasetName(e.target.value)}
        disabled={file && file.name.endsWith(".pdf")} // Disable for PDF
      />
      <input
        type="file"
        accept=".json,.pdf"
        onChange={handleFileChange}
      />
      <button onClick={handleUpload}>Upload and Fine-Tune</button>
      <p>Status: {status}</p>
      {downloadUrl && (
        <div>
          <a href={downloadUrl} download={`${datasetName || file.name}.zip`}>
            Download Fine-Tuned Model
          </a>
        </div>
      )}
    </div>
  );
}

export default FineTune;
