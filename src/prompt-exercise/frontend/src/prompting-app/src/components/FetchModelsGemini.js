import React, { useState } from "react";

const FetchGeminiModels = ({ apiKey }) => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchModels = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setModels(data.models); // Assuming the response contains a `models` array
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Gemini Models</h2>
      <button onClick={fetchModels} disabled={loading}>
        {loading ? "Loading..." : "Fetch Models"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {models.map((model) => (
          <li key={model.name}>
            <strong>{model.name}</strong>: {model.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FetchGeminiModels;
