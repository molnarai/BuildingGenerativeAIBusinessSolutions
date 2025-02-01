import React, { useState, useEffect } from 'react';
import './ResponseArchive.css';

const ResponseArchiveWidget = ({ problem, savedResponses, selectedProblemId,
  handleChangeSelectForSubmission
 }) => {
  const [sortOrder, setSortOrder] = useState('desc');
  const [modalData, setModalData] = useState(null);
  const [filteredResponses, setFilteredResponses] = useState([]);
  

  // Filter and sort responses when dependencies change
  useEffect(() => {
    const filtered = savedResponses.filter(
      response => response.problem_id === selectedProblemId
    );
    
    const sorted = [...filtered].sort((a, b) => {
      const comparison = new Date(b.response_ai_timestamp) - new Date(a.response_ai_timestamp);
      return sortOrder === 'desc' ? comparison : -comparison;
    });
    
    setFilteredResponses(sorted);
  }, [savedResponses, selectedProblemId, sortOrder]);

  // Truncate text helper
  const truncateText = (text, maxLength = 50) => {
    return text?.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
  };

  // Toggle sort order
  const toggleSortOrder = () => {
    setSortOrder(prev => prev === 'desc' ? 'asc' : 'desc');
  };


  const handleChangeSubmission = (e, response) => {
    console.log(`Checkbox changed for response ${response.uuid}`);
    // setResponseObject({ ...responseObject, select_for_submission: e.target.checked });
  };

  // Modal dialog component
  const Modal = ({ data, onClose }) => {
    if (!data) return null;

    function convertKeyToTitleCase(key) {
      const words = key.split('_');
      if (key === 'uuid') return words[0].toUpperCase() + words.slice(1).map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
      if (key === 'id') return words.map(word => word.toUpperCase()).join(' ');
      // return words.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
      return words.map(capitalize).join(' ');
    }
    
    function capitalize(str) {
      if (str === 'uuid') return 'UUID';
      if (str === 'id') return 'ID';
      if (str === 'ai') return 'AI';
      if (str === 'llm') return 'LLM';
      if (str === 'at') return 'at';
      if (str === 'for') return 'for';
      return str.charAt(0).toUpperCase() + str.slice(1);
    }

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <button className="modal-close" onClick={onClose}>×</button>
          <h2>Response Details</h2>
          <div className="modal-body">
            {Object.entries(data).map(([key, value]) => (
              <div key={key} className="modal-row">
                <strong>{convertKeyToTitleCase(key)}:</strong>
                <div>{typeof value === 'boolean' ? value.toString() : value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="response-archive">
      <div className="archive-header">
        <h2>Saved Responses</h2>
        <button onClick={toggleSortOrder}>
          Sort {sortOrder === 'desc' ? '↓' : '↑'}
        </button>
      </div>

      <div className="response-list">
        {filteredResponses.map((response) => (
          <div 
            key={response.uuid} 
            className="response-item"
            // onClick={() => setModalData(response)}
          >
            <div className="response-content" >
            <div className="model-info">
                {/* <strong>Provider:</strong> {response.response_ai_provider} | 
                <strong>Model:</strong> {response.response_ai_model} */}
                {response.response_ai_provider} | {response.response_ai_model}
              </div>
              
              <div 
                className="truncated-text" 
                title={response.response_prompt}
              >
                <strong>Prompt:</strong> {truncateText(response.response_prompt)}
              </div>
              
              <div 
                className="truncated-text" 
                title={response.response_llm_answer}
              >
                <strong>Response:</strong> {truncateText(response.response_llm_answer)}
              </div>
              
              
              {response.user_comment && (
                <div 
                  className="truncated-text" 
                  title={response.user_comment}
                >
                  <strong>Comment:</strong> {truncateText(response.user_comment)}
                </div>
              )}
              <label>
                <a href="#" 
                  onClick={() => setModalData(response)}
                >
                  More...
                </a>
              </label>
              <label className="submission-select">
                <input
                  type="checkbox"
                  checked={response.select_for_submission}
                  onChange={(e) => {
                    // Handle checkbox change - you'll need to implement this
                    // For now, just log the event
                    // console.log(`Checkbox changed for response ${response.uuid}`);
                    handleChangeSelectForSubmission(e.target.checked, response)
                    // response.select_for_submission = e.target.checked;
                    //e.stopPropagation();
                  }}
                />
                Select for submission
              </label>
              
            </div>
            {/* <label className="submission-select">
                <input
                  type="checkbox"
                  checked={response.select_for_submission}
                  onChange={(e) => handleChangeSubmission(e, response)}
                />
                Select for submission
              </label> */}
          </div>
        ))}
      </div>

      {modalData && (
        <Modal 
          data={modalData} 
          onClose={() => setModalData(null)} 
        />
      )}
    </div>
  );
};

export default ResponseArchiveWidget;
