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
                    <h2>Welcome to Our Application</h2>
                    <div className="help-modal-body">
                        <h3>Getting Started</h3>
                        <ul>
                            <li>Select The problme from the tab menu</li>
                            <li>Enter your prompt in the text area</li>
                            <li>Click "Submit" to get AI responses</li>
                            <li>Save responses you want to keep</li>
                            <li>Add comments to saved responses</li>
                        </ul>

                        <h3>Managing Responses</h3>
                        <ul>
                            <li>View your saved responses in the archive</li>
                            <li>Select responses for submission</li>
                            <li>Sort responses by timestamp</li>
                            <li>Click "See complete record" for full details</li>
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
