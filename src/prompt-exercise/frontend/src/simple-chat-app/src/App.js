/*
 * Copyright (c) 2025 Péter Molnár
 * LinkedIn: https://www.linkedin.com/in/petermolnar/
 *
 * This code is licensed under the Creative Commons license. 
 * You are free to use, modify, and distribute it as long as proper attribution is provided.
 * 
 * Authorship: Péter Molnár with assistance from AI tools.
 * 
 * Disclaimer: This code is provided "as is", without any guarantees of correctness or functionality.
 * Use it at your own risk. The author assumes no liability for any issues arising from its use.
 * 
 */

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './App.css';

// Get predefined values from environ variables (https://gist.github.com/Haugen/f6d685f18b4bd8a3cf5bcf6272577c5b)
// edit `../ .env` file to change values
const ai_application_name = process.env.REACT_APP_AI_APPLICATION_NAME;
const ai_application_url = process.env.REACT_APP_AI_APPLICATION_BASE_URL;
console.log(`AI_APPLICATION_BASE_URL=${ai_application_url}`);


function dashToTitle(str) {
  return str
    .split('-') // Split the string by underscores
    .map(word => word.length> 2 ? word.charAt(0).toUpperCase() + word.slice(1) : word.toUpperCase() ) // Capitalize the first letter of each word
    .join(' '); // Join the words with spaces
}


function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [endpoint, setEndpoint] = useState(`${ai_application_url}/v1/chat/completions`);
  const [useEndpoint, setUseEndpoint] = useState(false);
  const [languageModel, setLanguageModel] = useState('llama3.1');
  const [systemPrompt, setSystemPrompt] = useState('You are a helpful assistant.');
  const [llmTemperature, setLllmTemperature] = useState(0.0);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(scrollToBottom, [messages]);
  document.title = dashToTitle(ai_application_name); /* https://stackoverflow.com/questions/34834091/changing-the-document-title-in-react */

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // const response = await fetch(`${ai_application_url}/v1/chat/completions`, {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: languageModel,
          temperature: llmTemperature,
          messages: [...messages, userMessage],
          stream: true,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let aiResponse = { role: 'assistant', content: '' };
      setMessages(prevMessages => [...prevMessages, aiResponse]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              console.log('Stream finished');
            } else {
              try {
                const parsed = JSON.parse(data);
                const content = parsed.choices[0].delta.content;
                if (content) {
                  aiResponse.content += content;
                  setMessages(prevMessages => [
                    ...prevMessages.slice(0, -1),
                    { ...aiResponse }
                  ]);
                }
              } catch (error) {
                console.error('Error parsing JSON:', error);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prevMessages => [
        ...prevMessages,
        { role: 'system', content: 'An error occurred. Please try again.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>{dashToTitle(ai_application_name)}</h1>
      </header>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
             <strong>{message.role === 'user' ? 'You' : 'AI'}: </strong>
            {message.role === 'user'? (<span>{message.content}</span>)
            : (<ReactMarkdown remarkPlugins={[remarkGfm]} >{message.content}</ReactMarkdown>)}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={sendMessage} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
      <div style={{ height: '20px' }}></div>
      <form className="input-form">
        {/* <input
        type="checkbox"
        checked={useEndpoint}
        onChange={(e) => setUseEndpoint(e.target.checked)}
        disabled={isLoading}
      /> */}
      <label>Endpoint:</label>
      <input
          type="text"
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
          placeholder="Custom endpoint, e.g., http://localhost:8000"
          disabled={isLoading}
        />
      </form>
    </div>
  );
}

export default App;

