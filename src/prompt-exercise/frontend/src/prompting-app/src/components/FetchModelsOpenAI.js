import React, { useState } from "react";

const FetchModels = ({ apiKey }) => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchModels = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("https://api.openai.com/v1/models", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      // Filter for instruction-following models (e.g., GPT-4, GPT-3.5-turbo-instruct)
      const instructionModels = data.data.filter((model) =>
        model.id.includes("instruct") || model.id.includes("gpt")
      );
      setModels(instructionModels);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2>Fetch Available Instruction Models</h2>
      <button onClick={fetchModels} disabled={loading}>
        {loading ? "Loading..." : "Fetch Models"}
      </button>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {models.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h3>Instruction Models:</h3>
          <ul>
            {models.map((model) => (
              <li key={model.id}>
                <strong>{model.id}</strong>: {model.object}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FetchModels;
