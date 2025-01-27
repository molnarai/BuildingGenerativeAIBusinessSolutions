import React, { useState, useEffect } from "react";

// Mock FetchModel functions for each provider
const fetchOpenAIModels = async (apiKey) => {
    if (!apiKey) return [];
    var models = [];
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
        models = data.data
            .filter((model) =>
                model.id.includes("instruct") || model.id.includes("gpt")
            )
            .map((model) => model.id);
        console.log("OpenAI models fetched", models);
    } catch (err) {
        // setError(err.message);
        console.log("Error fetching models", err);
    } finally {
        console.log("Models fetched");
    }
    return models
};


const fetchGeminiModels = async (apiKey) => {
    if (!apiKey) return [];
    // Simulate API call
    return ["gemini-1.5-pro", "gemini-1.5-flash"];
    return [];
};

const fetchOllamaModels = async (baseUrl) => {
    if (!baseUrl) return [];
    var models = [];
    try {
        const response = await fetch(`${baseUrl}/v1/models`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        models = data.data.map((model) => model.id);
        console.log("Ollama models fetched", models);
    } catch (err) {
        console.log("Error fetching models", err.message);
    } finally {
        // setLoading(false);
        console.log("Models fetched");
    }
    return models;
};

const fetchLMStudioModels = async (baseUrl) => {
    if (!baseUrl) return [];
    var models = [];
    try {
        const response = await fetch(`${baseUrl}/v1/models`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        models = data.data.map((model) => model.id);
        console.log("LM-Studio models fetched", models);
    } catch (err) {
        console.log("Error fetching models", err.message);
    } finally {
        // setLoading(false);
        console.log("Models fetched");
    }
    return models;
};


const fetchGSUModels = async (baseUrl) => {
    if (!baseUrl) return [];
    var models = [];
    try {
        const response = await fetch(`${baseUrl}/v1/models`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            //throw new Error(`Error: ${response.statusText}`);
            return [];
        }

        const data = await response.json();
        models = data.data.map((model) => model.id);
        console.log("GSU models fetched", models);
    } catch (err) {
        console.log("Error fetching models", err.message);
    } finally {
        // setLoading(false);
        console.log("Models fetched");
    }
    return models;
};

// Define styles outside the component
const selectorStyles = {
    container: {
        padding: "20px",
        fontFamily: "Arial, sans-serif",
    },
    selectorsContainer: {
        display: "flex",
        gap: "20px",
        alignItems: "left",
    },
    selectorGroup: {
        flex: 1,
        display: "flex",
        alignItems: "left",
    },
    label: {
        whiteSpace: "nowrap",
        marginRight: "10px",
    },
    select: {
        flex: 1,
        padding: "5px",
    },
};

const ModelSelector = ({ config, onProviderModelChange }) => {
    const [modelData, setModelData] = useState([]);
    const [selectedProvider, setSelectedProvider] = useState("");
    const [selectedModel, setSelectedModel] = useState("");


    useEffect(() => {
        const fetchAllModels = async () => {
            const openAiApiKey = config.openAiApiKey;
            const geminiApiKey = config.geminiApiKey;
            const ollamaBaseUrl = config.ollamaBaseUrl
            const lmStudioBaseUrl = config.lmStudioBaseUrl;
            const gsuBaseUrl = config.gsuBaseUrl;
            // console.log("openAiApiKey", openAiApiKey);
            // console.log("geminiApiKey", geminiApiKey);
            // console.log("ollamaBaseUrl", ollamaBaseUrl);
            // console.log("lmStudioBaseUrl", lmStudioBaseUrl);

            const providers = [];
            if (openAiApiKey) {
                const openAIModels = await fetchOpenAIModels(openAiApiKey);
                if (openAIModels && openAIModels.length > 0) {
                    providers.push({ Provider: "OpenAI", Models: openAIModels });
                } else {
                    console.log("No OpenAI models found");
                }
            }

            if (geminiApiKey) {
                const geminiModels = await fetchGeminiModels(geminiApiKey);
                if (geminiModels && geminiModels.length > 0) {
                    providers.push({ Provider: "Gemini", Models: geminiModels });
                } else {
                    console.log("No Gemini models found");
                }
            }

            if (ollamaBaseUrl) {
                const ollamaModels = await fetchOllamaModels(ollamaBaseUrl);
                if (ollamaModels && ollamaModels.length > 0) {
                    providers.push({ Provider: "Ollama", Models: ollamaModels });
                } else {
                    console.log("No Ollama models found");
                }
            }

            if (lmStudioBaseUrl) {
                const lmStudioModels = await fetchLMStudioModels(lmStudioBaseUrl);
                if (lmStudioModels && lmStudioModels.length > 0) {
                    providers.push({ Provider: "LM Studio", Models: lmStudioModels });
                } else {
                    console.log("No LM-Studio models found");
                }
            }

            // if (gsuBaseUrl) {
            //     const gsuModels = await fetchGSUModels(gsuBaseUrl);
            //     if (gsuModels && gsuModels.length > 0) {
            //         providers.push({ Provider: "GSU", Models: gsuModels });
            //     } else {
            //         console.log("No GSU models found");
            //     }
            // }
            setModelData(providers);
        };

        fetchAllModels();
    }, [config, setSelectedModel, setSelectedProvider]);


    // Handle provider change
    const handleProviderChange = (provider) => {
        setSelectedProvider(provider);
        setSelectedModel(""); // Reset model selection when provider changes
        onProviderModelChange(provider, "");
    };

    // Handle model change
    const handleModelChange = (model) => {
        setSelectedModel(model);
        onProviderModelChange(selectedProvider, model);
    };

    return (
        <div style={selectorStyles.container}>
            <div style={selectorStyles.selectorsContainer}>
                {/* Provider Dropdown */}
                <div style={selectorStyles.selectorGroup}>
                    <label style={selectorStyles.label}>
                        <strong>Provider:</strong>
                    </label>
                    <select
                        value={selectedProvider}
                        onChange={(e) => handleProviderChange(e.target.value)}
                        style={selectorStyles.select}
                    >
                        <option value="">Select a provider</option>
                        {modelData.map((provider) => (
                            <option key={provider.Provider} value={provider.Provider}>
                                {provider.Provider}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Model Dropdown */}
                <div style={selectorStyles.selectorGroup}>
                    <label style={selectorStyles.label}>
                        <strong>Model:</strong>
                    </label>
                    <select
                        value={selectedModel}
                        onChange={(e) => handleModelChange(e.target.value)}
                        style={selectorStyles.select}
                        disabled={!selectedProvider}
                    >
                        <option value="">Select a model</option>
                        {selectedProvider &&
                            modelData
                                .find((provider) => provider.Provider === selectedProvider)
                                ?.Models.map((model) => (
                                    <option key={model} value={model}>
                                        {model}
                                    </option>
                                ))}
                    </select>
                </div>
            </div>
        </div>
    );
};

export default ModelSelector;
