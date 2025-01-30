import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const InstructionsWidget = ({ problem }) => {
  // console.log("InstructionsWidget", problem);
  let description = problem?.description.replace(/\\n/g, "\n") || "No description available";
  let title = problem?.title || "No title available";
  return (
    <div className="instructions-widget">
      <h2>{title}</h2>
      <ReactMarkdown 
        children={description} 
        remarkPlugins={[remarkGfm]}
      />
    </div>
  );
};

export default InstructionsWidget;
