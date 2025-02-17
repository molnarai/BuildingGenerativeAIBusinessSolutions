import React, { useState, useEffect } from 'react';
import './HelpWidget.css';

const HelpWidget = ({ isOpen, onClose }) => {
    const [dontShowAgain, setDontShowAgain] = useState(false);

    const handleClose = () => {
        if (dontShowAgain) {
            localStorage.setItem('hideHelpWidget', 'true');
        }
        onClose();
    };

    return (
        isOpen && (
            <div className="help-modal-overlay">
                <div className="help-modal-content">
                    <button className="help-modal-close" onClick={handleClose}>×</button>
                    <h2>Homework 1</h2>
                    <div className="help-modal-body">
                        Visit the <a 
                        href={"https://molnarai.github.io/BuildingGenerativeAIBusinessSolutions/assignments/assignment-01/"}
                        target="_blank"
                        >
                            Homework 1 
                        </a> page on the class details of this  assignment.
                        <h3>Setup LLM Model Providers</h3>
                        <ul>
                        <li>You can select the "GSU" as the model provider. Though, this provider supports only selected models.
                             You may choose to setup an OpenAI key for a variety of LLMs, or even host your own LLM server (Ollama or LM Notebook). Visit the homework page
                             for information on how to setup these applications.
                        </li>
                        <li>
                            Enter your API key and URLs for your local providers in the "Configuration Sessings" on the lower left of the screen.
                        </li>
                        </ul>
                        <h3>Getting Started</h3>
                        <ol>
                            <li>Select the problem from the tab menu on the top of the screen. The instructions show up on the left.</li>
                            <li>Chose a model provider and model from the dropdowns. Adjust the parameters like temperature and maximum number of tokens.</li>
                            <li>Enter your prompt in the text area and click "Submit" to get AI responses.</li>
                            <li>Add an observation to the response and click "Save Response" to save the response. You cannot save responses without comment.</li>
                        </ol>
                
                        <h3>Managing Responses for Grading</h3>
                        <ul>
                            <li>You can view your saved items in the "Saved Responses" panel on the right. Click on "See complete record..." for all data.</li>
                            <li>You need to select responses for grading. After experimentation, pick the ones that align best with the problem statement. If more than the required number of 
                                responses are selected, the oldest responses will be ignored.
                            </li>
                            <li>The "Completion Summary" provides a count of your responses.</li>
                            <li>You can create new responses and change your selection at any time as long as the assignment is open.</li>
                        </ul>

                        <div className="dont-show-again">
                            <label>
                                <input
                                    type="checkbox"
                                    checked={dontShowAgain}
                                    onChange={(e) => setDontShowAgain(e.target.checked)}
                                />
                                Don't show this again
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        )
    );
};

export default HelpWidget;
