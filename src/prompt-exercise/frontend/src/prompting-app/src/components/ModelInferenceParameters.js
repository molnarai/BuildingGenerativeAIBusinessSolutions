import React, { useState } from 'react';

const styles = {
  container: {
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  controlGroup: {
    display: "flex",
    alignItems: "center",
    marginBottom: "15px",
    gap: "10px",
  },
  label: {
    whiteSpace: "nowrap",
    minWidth: "120px",
  },
  input: {
    flex: 1,
    padding: "5px",
  },
  slider: {
    flex: 1,
  },
  value: {
    marginLeft: "10px",
    minWidth: "50px",
  }
};

const ModelInferenceParameters = ({ parameters, setParameters }) => {
  // const [parameters, setParameters] = useState({
  //   stream: true,
  //   temperature: 0.0,
  //   max_tokens: 1000
  // });

  const handleLLMParametersChange = (parameters) => {
    //console.log(`Inference parameters changed: ${JSON.stringify(parameters)}`);
};
  const handleStreamChange = (e) => {
    const newParameters = {
      ...parameters,
      stream: e.target.checked
    };
    setParameters(newParameters);
    handleLLMParametersChange(newParameters);
  };

  const handleTemperatureChange = (e) => {
    const newParameters = {
      ...parameters,
      temperature: parseFloat(e.target.value)
    };
    setParameters(newParameters);
    handleLLMParametersChange(newParameters);
  };

  const handleMaxTokensChange = (e) => {
    const newParameters = {
      ...parameters,
      max_tokens: parseInt(e.target.value, 10) || 0
    };
    setParameters(newParameters);
    handleLLMParametersChange(newParameters);
  };

  return (
    <div style={styles.container}>
      {/* Stream Checkbox */}
      <div style={styles.controlGroup}>
        <label style={styles.label}>
          <strong>Stream Response:</strong>
        </label>
        <input
          type="checkbox"
          checked={parameters.stream}
          onChange={handleStreamChange}
        />
      </div>

      {/* Temperature Slider */}
      <div style={styles.controlGroup}>
        <label style={styles.label}>
          <strong>Temperature:</strong>
        </label>
        <input
          type="range"
          min="0"
          max="1.0"
          step="0.1"
          value={parameters.temperature}
          onChange={handleTemperatureChange}
          style={styles.slider}
        />
        <span style={styles.value}>{parameters.temperature.toFixed(1)}</span>
      </div>

      {/* Max Tokens Input */}
      <div style={styles.controlGroup}>
        <label style={styles.label}>
          <strong>Max Tokens:</strong>
        </label>
        <input
          type="number"
          min="1"
          value={parameters.max_tokens}
          onChange={handleMaxTokensChange}
          style={styles.input}
        />
      </div>
    </div>
  );
};

export default ModelInferenceParameters;
