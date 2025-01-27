import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import ModelSelector from "./ModelSelector";
import ModelInferenceParameters from "./ModelInferenceParameters";

const AIAssistantWidget = ({ apiKey, apiUrl, config, userInfo, problemDetails }) => {
    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [userComment, setUserComment] = useState("");
    const [stats, setStats] = useState({ time: 0, inputTokens: 0, outputTokens: 0, totalTokens: 0 });
    const [isLoading, setIsLoading] = useState(false);
    const responseRef = useRef("");
    const [selectedProviderModel, setSelectedProviderModel]
        = useState({ "provider": "openai", "model": "gpt-4" });

    const [parameters, setParameters] = useState({
        "stream": false,
        // "top_p": 1.0,
        // "presence_penalty": 0.0,
        "temperature": 0.0,
        "max_tokens": 1000
    });

    const [aiResponse, setAiResponse] = useState({
        "problem_id": 0,                    // = Column(Integer, ForeignKey("problems.id"), nullable=False)
        "user_id": 0,                       // = Column(Integer, ForeignKey("users.id"))
        "response_prompt": "",              // = Column(String, nullable=False)
        "response_llm_answer": "",          // = Column(String, nullable=False)
        "response_ai_provider": "",         // = Column(String, nullable=False)
        "response_ai_model": "",            // = Column(String, nullable=False)
        "response_ai_input_tokens": 0,      // = Column(Integer, nullable=False)
        "response_ai_output_tokens": 0,     //  = Column(Integer, nullable=False)
        "response_ai_seconds": 0,           // = Column(Integer, nullable=False)
        "created_at": "",                   // = Column(DateTime(timezone=True), server_default=func.now())
        "select_for_submission": false,     // = Column(Boolean, default=False)
        "submission_time": "",              //  = Column(DateTime(timezone=True))
    });

    // const updateAiResponse = async (prompt, metadata) => {
    //     setAiResponse({
    //         ...aiResponse,
    //         response_llm_answer: response.llmAnswer,
    //         response_ai_provider: response.aiProvider,
    //         response_ai_model: response.aiModel,
    //         response_ai_input_tokens: response.inputTokens,
    //         response_ai_output_tokens: response.outputTokens,
    //         response_ai_seconds: response.seconds
    //     });
    //             user_id: userId,
    //             response_prompt: responsePrompt,
    //             response_llm_answer: response.llmAnswer,
    //             response_ai_provider: response.aiProvider,
    //             response_ai_model: response.aiModel,
    //             response_ai_input_tokens: response.inputTokens,
    //             response_ai_output_tokens: response.outputTokens,
    //             response_ai_seconds: response.seconds,
    //             created_at: new Date(),
    //             select_for_submission: false,
    //             submission_time: ""
    //         });


    const handleProviderModelChange = (provider, model) => {
        setSelectedProviderModel({ "provider": provider, "model": model });
        console.log(`Selected provider model: ${provider} - ${model}`);
    };

    

    //   _   _                 _ _        ____                                      
    //  | | | | __ _ _ __   __| | | ___  |  _ \ ___  ___ _ __   ___  _ __  ___  ___ 
    //  | |_| |/ _` | '_ \ / _` | |/ _ \ | |_) / _ \/ __| '_ \ / _ \| '_ \/ __|/ _ \
    //  |  _  | (_| | | | | (_| | |  __/ |  _ <  __/\__ \ |_) | (_) | | | \__ \  __/
    //  |_| |_|\__,_|_| |_|\__,_|_|\___| |_| \_\___||___/ .__/ \___/|_| |_|___/\___|
    //                                                  |_|                         

    const handleResponse = async (response, onChunk) => {
        let metadata = {
            id: '',
            object: 'text_completion',
            created: Math.floor(Date.now() / 1000),
            model: '',
            choices: [{
              text: '',
              finish_reason: null
            }],
            usage: {
              completion_tokens: 0,
              prompt_tokens: 0,
              total_tokens: 0
            }
        };

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response no-streaming data:", data);

        // Handle both chat completion and text completion responses
        if (data.choices && data.choices.length > 0) {
            // Chat completion response
            if (data.choices[0].message?.content !== undefined) {
                // return data.choices[0].message.content;
                onChunk(data.choices[0].message.content);
            }
            // Text completion response
            else if (data.choices[0].text !== undefined) {
                //return data.choices[0].text;
                onChunk(data.choices[0].text);
            }
            else {
                throw new Error('Unexpected response structure from API');
            }
        }
        metadata.choices = data.choices;
        metadata.usage = data.usage;
        metadata.id = data.id;
        metadata.model = data.model;
        return metadata
    };


    // Modified handleStreamingResponse to accept a callback
    const handleStreamingResponse = async (response, onChunk) => {
        let accumulatedText = '';
        let metadata = {
            id: '',
            object: 'text_completion',
            created: Math.floor(Date.now() / 1000),
            model: '',
            choices: [{
              text: '',
              finish_reason: null
            }],
            usage: {
              completion_tokens: 0,
              prompt_tokens: 0,
              total_tokens: 0
            }
        };
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let completion_tokens = 0;
        
        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    metadata.choices[0].text = accumulatedText;
                    metadata.choices[0].finish_reason = 'stop';
                    break;
                }
                //console.log("Response streaming data:", value);
                

                const chunk = decoder.decode(value);
                
                
                try {
                    const parsedChunk = JSON.parse(chunk.replace(/^data:\s+/, ''));
                    // console.log("Response streaming parsedChunk:", parsedChunk);
                    if (parsedChunk.id) metadata.id = parsedChunk.id;
                    if (parsedChunk.model) metadata.model = parsedChunk.model;
                    if (parsedChunk.usage) metadata.usage = parsedChunk.usage;
                    
                    // Accumulate the text content
                    if (parsedChunk.choices && parsedChunk.choices[0].text) {
                        accumulatedText += parsedChunk.choices[0].text;
                    }
                } catch (error) {
                    console.log("Error parsing response chunk:", error);
                };
                
       
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.trim() === '') continue;
                    if (line.includes('[DONE]')) continue;

                    if (line.startsWith('data: ')) {
                        try {
                            const jsonString = line.replace('data: ', '');
                            const parsed = JSON.parse(jsonString);

                            // Handle both chat and completion responses
                            const content = parsed.choices?.[0]?.delta?.content || // chat completion
                                parsed.choices?.[0]?.text || ''; // text completion

                            if (content) {
                                completion_tokens += 1;
                                onChunk(content);
                                // Force React to re-render immediately
                                await new Promise(resolve => setTimeout(resolve, 0));
                            }
                        } catch (e) {
                            console.error('Error parsing chunk:', e);
                            continue;
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error in streaming:', error);
        }
        if (! metadata.usage.completion_tokens)
            metadata.usage.completion_tokens = completion_tokens;
        if (! metadata.usage.prompt_tokens)
            metadata.usage.prompt_tokens = prompt.split(" ").length;
        if (! metadata.usage.total_tokens) 
            metadata.usage.total_tokens = completion_tokens + metadata.usage.prompt_tokens;
        
        return metadata;

    };

    //   _   _                 _ _        ____        _               _ _   
    //  | | | | __ _ _ __   __| | | ___  / ___| _   _| |__  _ __ ___ (_) |_ 
    //  | |_| |/ _` | '_ \ / _` | |/ _ \ \___ \| | | | '_ \| '_ ` _ \| | __|
    //  |  _  | (_| | | | | (_| | |  __/  ___) | |_| | |_) | | | | | | | |_ 
    //  |_| |_|\__,_|_| |_|\__,_|_|\___| |____/ \__,_|_.__/|_| |_| |_|_|\__|


    const handleSubmit = async () => {
        setIsLoading(true);
        setResponse("");
        responseRef.current = "";

        const startTime = Date.now();
        let res;
        try {

            if (selectedProviderModel.provider.toLowerCase() === "openai") {
                res = await fetch('https://api.openai.com/v1/chat/completions', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${config.openAiApiKey}`,
                    },
                    body: JSON.stringify({
                        messages: [
                            {
                                role: "user",
                                content: prompt,
                            },
                        ],
                        temperature: parameters.temperature,
                        model: selectedProviderModel.model, // Adjust based on your model
                        max_tokens: parameters.maxTokens,
                        stream: parameters.stream,
                    }),
                });
            } else if (selectedProviderModel.provider.toLowerCase() === "ollama") {
                res = await fetch(`${config.ollamaBaseUrl}/v1/completions`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${apiKey}`,
                    },
                    body: JSON.stringify({
                        prompt,
                        model: selectedProviderModel.model, // Adjust based on your model
                        max_tokens: parameters.max_tokens,
                        temperature: parameters.temperature,
                        stream: parameters.stream,
                    }),
                });
            } else if (selectedProviderModel.provider.toLowerCase().replaceAll(" ", "") === "lmstudio") {
                //apiUrl = "http://localhost:1234/v1/chat/completions";
                res = await fetch(`${config.lmStudioBaseUrl}/v1/completions`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        // Authorization: `Bearer ${apiKey}`,
                    },
                    body: JSON.stringify({
                        prompt,
                        model: selectedProviderModel.model, // Adjust based on your model
                        max_tokens: parameters.max_tokens,
                        temperature: parameters.temperature,
                        stream: parameters.stream,
                    }),
                });
            } else if (selectedProviderModel.provider.toLowerCase() === "gemini") {
                res = await fetch(apiUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${apiKey}`,
                    },
                    body: JSON.stringify({
                        prompt,
                        model: "text-davinci-003", // Adjust based on your model
                        max_tokens: 100,
                        stream: true,
                    }),
                });
            } else {
                throw new Error("Unsupported provider");
            }


            if (!res.body) throw new Error("No response body");
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            let content;
            let metadata = {};

            //let responseRef = useRef("");
            console.log("Handle Stream?:", parameters.stream);
            if (parameters.stream) {
                metadata = await handleStreamingResponse(res, (chunk) => {
                    responseRef.current += chunk;
                    //setResponse(responseRef.current);
                    setResponse(prev => prev + chunk);
                });
                content = responseRef.current;
            } else {
                metadata = await handleResponse(res, (content) => {
                    responseRef.current = content;
                    setResponse(content);
                    //setResponse(responseRef.current);
                    //setResponse(prev => prev + chunk);
                });
                // responseRef.current = content;
                // setResponse(content);
                content = responseRef.current;
            }
            
            console.log("AI response Metadata:", metadata);
            setAiResponse({...aiResponse,
                problem_id: problemDetails.problem_id,
                problem_title: problemDetails.title,
                problem_description: problemDetails.description,
                response_prompt: prompt,
                response_llm_answer: content,
                response_ai_provider: selectedProviderModel.provider,
                response_ai_model: selectedProviderModel.model,
                response_ai_input_tokens: metadata.usage.prompt_tokens,
                response_ai_output_tokens: metadata.usage.completion_tokens,
                response_ai_seconds: (Date.now() - startTime) / 1000,
            });
            

            const elapsedTime = Date.now() - startTime;
            setStats({
                time: elapsedTime,
                inputTokens: prompt.split(" ").length,
                outputTokens: content.split(" ").length,
            });
        } catch (error) {
            console.error("Error fetching AI response:", error);
        } finally {
            setIsLoading(false);
            
        }
    };

    const handleSaveResponse = () => {
        // const userComment = promptInputRef.current.value;
        console.log("Saving AI-Response:", aiResponse);
        // Handle saving the comment (e.g., API call or local storage)
    };

    useEffect(() => {
        // Force re-render when response changes
        const element = document.querySelector('.response-container');
        if (element) {
            element.scrollTop = element.scrollHeight;
        }
    }, [response]);
    

    return (
        <div style={{
            maxWidth: "1600px", margin: "0 auto", padding: "20px",
            border: "1px solid #ddd", textAlign: "left"
        }}>
            <h2>AI Assistant</h2>
            <ModelSelector
                config={config}
                onProviderModelChange={handleProviderModelChange}
            />
            <ModelInferenceParameters
               parameters={parameters}
                setParameters={setParameters}
            />
            {/* <div style={{ marginBottom: "20px" }}>
                <label htmlFor="userComment">User Comment:</label>
                <textarea
                    id="userComment"
                    value={userComment}
                    onChange={(e) => setUserComment(e.target.value)}
                    placeholder="Enter your comment here..."
                    rows="4"
                    style={{ width: "100%" }}
                />
            </div> */}
            {/* Prompt Input */}
            <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your prompt here..."
                rows="20"
                style={{ width: "100%", marginBottom: "10px" }}
            />

            <button onClick={handleSubmit} disabled={isLoading}>
                {isLoading ? "Loading..." : "Submit"}
            </button>

            {/* Response Display */}
            <div className="response-container" style={{ marginTop: "20px", padding: "10px", border: "1px solid #ddd", backgroundColor: "#f9f9f9" }}>
                <h3>AI Response:</h3>
                <ReactMarkdown
                    //  children={response.choices[0].message.content.replace('\\n', '\n')}
                    children={response}
                    remarkPlugins={[remarkGfm]}
                />
            </div>

            {/* User Comment */}
            <textarea
                value={userComment}
                onChange={(e) => setUserComment(e.target.value)}
                placeholder="Write your comment here..."
                rows="3"
                style={{ width: "100%", marginTop: "10px" }}
            />

            <button onClick={handleSaveResponse} style={{ marginTop: "10px" }}>
                Save Response
            </button>

            {/* Stats Display */}
            <div style={{ marginTop: "20px", fontSize: "14px" }}>
                <p><strong>Response Time:</strong> {stats.time} ms</p>
                <p><strong>Input Tokens:</strong> {stats.inputTokens}</p>
                <p><strong>Output Tokens:</strong> {stats.outputTokens}</p>
            </div>
        </div>
    );
};

export default AIAssistantWidget;
