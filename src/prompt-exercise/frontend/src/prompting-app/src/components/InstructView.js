// src/components/InstructView.js
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function InstructView({ endpoint, languageModel, llmTemperature }) {
  const [instruction, setInstruction] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!instruction.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: languageModel,
          temperature: llmTemperature,
          messages: [{ role: 'user', content: instruction }],
          stream: true,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';

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
                  fullResponse += content;
                  setResponse(fullResponse);
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
      setResponse('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="instruct-view">
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={instruction}
          onChange={(e) => setInstruction(e.target.value)}
          placeholder="Enter your instruction..."
          disabled={isLoading}
          rows={4}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Submit'}
        </button>
      </form>
      {response && (
        <div className="response-container">
          <h3>Response:</h3>
          <div className="response">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{response}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}

export default InstructView;
