import React, { useState, useEffect } from "react";

const ConfigurationWidget = ({ config, handleInputChange, handleDeleteConfiguration }) => {
  // // State for configuration fields
  // const [config, setConfig] = useState({
  //   openAiApiKey: "",
  //   geminiApiKey: "",
  //   ollamaBaseUrl: "",
  //   lmStudioBaseUrl: "",
  //   temperature: 0.0,
  //   topP: 1.0,
  //   maxTokens: 1000,
  // });

  // State for visibility toggles
  const [visibility, setVisibility] = useState({
    openAiApiKey: false,
    geminiApiKey: false,
  });

  // // Load configuration from localStorage on component mount
  // useEffect(() => {
  //   const savedConfig = {
  //     openAiApiKey: localStorage.getItem("openAiApiKey") || "",
  //     geminiApiKey: localStorage.getItem("geminiApiKey") || "",
  //     ollamaBaseUrl: localStorage.getItem("ollamaBaseUrl") || "",
  //     lmStudioBaseUrl: localStorage.getItem("lmStudioBaseUrl") || "",
  //     temperature: parseFloat(localStorage.getItem("temperature")) || 0.0,
  //     topP: parseFloat(localStorage.getItem("topP")) || 1.0,
  //     maxTokens: parseInt(localStorage.getItem("maxTokens"), 10) || 1000,
  //   };
  //   setConfig(savedConfig);
  // }, []);

  // // Handle input changes and update localStorage instantly
  // const handleInputChange = (key, value) => {
  //   setConfig((prev) => {
  //     const updatedConfig = { ...prev, [key]: value };
  //     localStorage.setItem(key, value); // Update localStorage
  //     return updatedConfig;
  //   });
  // };

  // Toggle visibility of sensitive fields
  const toggleVisibility = (key) => {
    setVisibility((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px", border: "1px solid #ddd" }}>
      <h2>Configuration Settings</h2>

      {/* OpenAI API Key */}
      <div style={{ marginBottom: "20px" }}>
        <label>
          <strong>OpenAI API Key:</strong>
        </label>
        <div style={{ display: "flex", alignItems: "center" }}>
          <input
            type={visibility.openAiApiKey ? "text" : "password"}
            value={config.openAiApiKey}
            onChange={(e) => handleInputChange("openAiApiKey", e.target.value)}
            placeholder="Enter OpenAI API Key"
            style={{ flexGrow: 1, marginRight: "10px" }}
          />
          <button className="smaller-button" onClick={() => toggleVisibility("openAiApiKey")}>
            {visibility.openAiApiKey ? "Hide" : "Show"}
          </button>
        </div>
      </div>

      {/* Gemini API Key */}
      <div style={{ marginBottom: "20px" }}>
        <label>
          <strong>Gemini API Key:</strong>
        </label>
        <div style={{ display: "flex", alignItems: "center" }}>
          <input 
            disabled={true}
            type={visibility.geminiApiKey ? "text" : "password"}
            value={config.geminiApiKey}
            onChange={(e) => handleInputChange("geminiApiKey", e.target.value)}
            placeholder="Enter Gemini API Key"
            style={{ flexGrow: 1, marginRight: "10px" }}
          />
          <button disabled={true} className="smaller-button"  onClick={() => toggleVisibility("geminiApiKey")}>
            {visibility.geminiApiKey ? "Hide" : "Show"}
          </button>
        </div>
      </div>

      {/* Ollama Base URL */}
      <div style={{ marginBottom: "20px" }}>
        <label>
          <strong>Ollama Base URL:</strong>
        </label>
        <input
          type="text"
          value={config.ollamaBaseUrl}
          onChange={(e) => handleInputChange("ollamaBaseUrl", e.target.value)}
          placeholder="Enter URL of your local Ollama server, e.g. http://localhost:11434"
          style={{ width: "90%" }}
        />
      </div>

      {/* LM Studio Base URL */}
      <div style={{ marginBottom: "20px" }}>
        <label>
          <strong>LM Studio Base URL:</strong>
        </label>
        <input
          // disabled={true}
          type="text"
          value={config.lmStudioBaseUrl}
          onChange={(e) => handleInputChange("lmStudioBaseUrl", e.target.value)}
          placeholder="Enter URL of your local LM-Studio server, e.g.http://localhost:8080"
          style={{ width: "90%" }}
        />
      </div>

      {/* Summary */}
      <p style={{ fontSize: "12px", color: "#555" }}>
        Your settings are saved locally in your browser and will persist across visits.
        <button
        onClick={() => {
          const isConfirmed = window.confirm("Are you sure you want to delete this configuration?");
          if (isConfirmed) {handleDeleteConfiguration()};
          }}
        className="smaller-button"
        >
          Clear Settings
        </button>
      </p>
    </div>
  );
};

export default ConfigurationWidget;
