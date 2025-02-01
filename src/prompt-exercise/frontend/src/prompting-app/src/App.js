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
import React, { useState, useRef, useEffect, use } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import AssignmentTabs from './components/AssignmentTabs';
import ChatView from './components/ChatView';
import InstructView from './components/InstructView';
import InstructionsWidget from './components/InstructionsWidget';
import ConfigurationWidget from './components/ConfigurationWidget';
import AIAssistantWidget from './components/AIAssistantWidget';
import LoginScreen from './components/LoginScreen';
import LoginStatusWidget from './components/LoginStatusWidget';
import ResponseArchiveWidget from './components/ResponseArchiveWidget';

import './App.css';

// Get predefined values from environ variables (https://gist.github.com/Haugen/f6d685f18b4bd8a3cf5bcf6272577c5b)
// edit `../ .env` file to change values

// console.log({
//   appName: process.env.REACT_APP_AI_APPLICATION_NAME,
//   ollamaUrl: process.env.REACT_APP_OLLAMA_BASE_URL,
//   appBaseUrl: process.env.REACT_APP_AI_APPLICATION_BASE_URL
// });
const ai_application_name = process.env.REACT_APP_AI_APPLICATION_NAME ? process.env.REACT_APP_AI_APPLICATION_NAME : 'prompting-assignment';
const ai_application_url = process.env.REACT_APP_AI_APPLICATION_BASE_URL ? process.env.REACT_APP_AI_APPLICATION_BASE_URL : 'http://localhost:8000';

console.log('AI Application Name:', process.env.REACT_APP_AI_APPLICATION_NAME);
console.log(`AI_APPLICATION_BASE_URL=${ai_application_url}`);

function dashToTitle(str) {
    return str
        .split('-') // Split the string by underscores
        .map(word => word.length > 2 ? word.charAt(0).toUpperCase() + word.slice(1) : word.toUpperCase()) // Capitalize the first letter of each word
        .join(' '); // Join the words with spaces
}

function App() {
    const [endpoint, setEndpoint] = useState(`${ai_application_url}/v1/chat/completions`);
    const [languageModel, setLanguageModel] = useState('llama3.1');
    const [llmTemperature, setLllmTemperature] = useState(0.0);
    // remove this: const [activeView, setActiveView] = useState('chat');


    //   _   _               ___       __     
    //  | | | |___ ___ _ _  |_ _|_ _  / _|___ 
    //  | |_| (_-</ -_) '_|  | || ' \|  _/ _ \
    //   \___//__/\___|_|   |___|_||_|_| \___/

    // remove this: const [username, setUsername] = useState(localStorage.getItem('username'));
    const [userInfo, setUserInfo] = useState({
        username: localStorage.getItem('username'),
        email: localStorage.getItem('email'),
        first_name: localStorage.getItem('first_name'),
        last_name: localStorage.getItem('last_name'),
        full_name: localStorage.getItem('full_name'),
        user_id: localStorage.getItem('user_id'),
        is_authenticated: localStorage.getItem('is_authenticated') === 'true',
        is_admin: localStorage.getItem('is_admin') === 'true',
        auth_token: localStorage.getItem('auth_token')
    });

    const handleLoginSuccess = (user) => {
        setUserInfo(user);
    };

    const handleLogout = () => {
        setUserInfo({ ...userInfo, is_authenticated: false, auth_token: null });
        // localStorage.removeItem('username');
        // localStorage.removeItem('email');
        // localStorage.removeItem('first_name');
        // localStorage.removeItem('last_name');
        // localStorage.removeItem('full_name');
        localStorage.removeItem('user_id');
        localStorage.removeItem('is_authenticated');
        localStorage.removeItem('is_admin');
        localStorage.removeItem('auth_token')
    };

    // Add this function to check if user is authenticated
    const isAuthenticated = () => {
        return true;
        // return !!localStorage.getItem('authToken');
    };


    //     _          _                         _     ___         _    _              
    //    /_\   _____(_)__ _ _ _  _ __  ___ _ _| |_  | _ \_ _ ___| |__| |___ _ __  ___
    //   / _ \ (_-<_-< / _` | ' \| '  \/ -_) ' \  _| |  _/ '_/ _ \ '_ \ / -_) '  \(_-<
    //  /_/ \_\/__/__/_\__, |_||_|_|_|_\___|_||_\__| |_| |_| \___/_.__/_\___|_|_|_/__/
    //                 |___/                                                          

    const [problems, setProblems] = useState([]);
    const [selectedTab, setSelectedTab] = useState(0); // Default to the first tab
    const [problemDetails, setProblemDetails] = useState({});

    // Fetch problems from the API
    useEffect(() => {
        const fetchProblems = async () => {
            try {
                const response = await fetch("http://localhost:8000/assignment/problems");
                if (!response.ok) {
                    throw new Error("Failed to fetch problems");
                }
                const data = await response.json();
                setProblems(data.problems);
            } catch (error) {
                console.error("Error fetching problems:", error);
            }
        };

        fetchProblems();
        let index = 0
        // setProblemDetails({
        //   problem_id: problems[index].id,
        //   title: problems[index].title,
        //   description: problems[index].description,
        //   number: index+1,
        // })
    }, []);


    useEffect(() => {
        if (problems.length > 0) {
            setProblemDetails({
                problem_id: problems[selectedTab].id,
                title: problems[selectedTab].title,
                description: problems[selectedTab].description,
                number: selectedTab + 1,
            });
        }
    }, [problems, selectedTab]);


    // Handle tab selection
    const onAssignmentTabClick = (index) => {
        setSelectedTab(index);
        setProblemDetails({
            problem_id: problems[index].id,
            title: problems[index].title,
            description: problems[index].description,
            number: index + 1,
        })
    };

    //    ___           __ _                    _   _          
    //   / __|___ _ _  / _(_)__ _ _  _ _ _ __ _| |_(_)___ _ _  
    //  | (__/ _ \ ' \|  _| / _` | || | '_/ _` |  _| / _ \ ' \ 
    //   \___\___/_||_|_| |_\__, |\_,_|_| \__,_|\__|_\___/_||_|
    //                      |___/                              
    /***** Configuration Widget */
    // Load configuration from localStorage on component mount

    // State for configuration fields
    const [config, setConfig] = useState({
        openAiApiKey: "",
        geminiApiKey: "",
        ollamaBaseUrl: "",
        lmStudioBaseUrl: "",
        gsuBaseUrl: ai_application_url,
        temperature: 0.0,
        topP: 1.0,
        maxTokens: 1000,
    });

    useEffect(() => {
        const savedConfig = {
            openAiApiKey: localStorage.getItem("openAiApiKey") || "",
            geminiApiKey: localStorage.getItem("geminiApiKey") || "",
            ollamaBaseUrl: localStorage.getItem("ollamaBaseUrl") || "",
            lmStudioBaseUrl: localStorage.getItem("lmStudioBaseUrl") || "",
            temperature: parseFloat(localStorage.getItem("temperature")) || 0.0,
            topP: parseFloat(localStorage.getItem("topP")) || 1.0,
            maxTokens: parseInt(localStorage.getItem("maxTokens"), 10) || 1000,
        };
        setConfig(savedConfig);
    }, []);

    // Handle input changes and update localStorage instantly
    const handleConfigurationInputChange = (key, value) => {
        setConfig((prev) => {
            const updatedConfig = { ...prev, [key]: value };
            localStorage.setItem(key, value); // Update localStorage
            return updatedConfig;
        });
    };


    //      _             _     _           
    //     / \   _ __ ___| |__ (_)_   _____ 
    //    / _ \ | '__/ __| '_ \| \ \ / / _ \
    //   / ___ \| | | (__| | | | |\ V /  __/
    //  /_/   \_\_|  \___|_| |_|_| \_/ \___|
                                         
    const [savedResponses, setSavedResponses] = useState([]);
    const [queuedResponses, setQueuedResponses] = useState([]);

    useEffect(() => {
        const localSavedResponses = JSON.parse(localStorage.getItem('savedResponses') || '[]');
        const localQueuedResponses = JSON.parse(localStorage.getItem('queuedResponses') || '[]');
        setSavedResponses(localSavedResponses);
        setQueuedResponses(localQueuedResponses);
    }, []);
    
    const handleAddResponseToArchive = (response) => {
        if (!response) return; // Ignore empty responses
        // test if record with uuid exists in savedResponses
        console.log("Response record:", response);
        if (savedResponses.find((r) => r.uuid === response.uuid)) {
            console.log("Duplicate response found:", response.uuid);
            return; // Ignore duplicate responses
        } else {
            setSavedResponses((prev) => [...prev, response]);
            localStorage.setItem('savedResponses', JSON.stringify(savedResponses));
            setQueuedResponses((prev) => [...prev, response]); // Add to queued responses
            console.log("Number of Saved Responses:", savedResponses.length);
            console.log("Number of Queued Responses:", queuedResponses.length);
        }
    }
    
    const handleChangeSelectForSubmission = (checked, response) => {
        console.log("Change Select for Submission: ", checked, response.uuid);
        setQueuedResponses((prev) => [...prev, response]); // Add to queued responses
        console.log("Number of Saved Responses:", savedResponses.length);
        console.log("Number of Queued Responses:", queuedResponses.length);
        const updatedResponses = savedResponses.map(r => 
            r.uuid === response.uuid 
              ? { ...r, select_for_submission: checked }
              : r
          );
        setSavedResponses(updatedResponses); // Assuming you have this state setter
        localStorage.setItem('savedResponses', JSON.stringify(savedResponses));
    }
    
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    <h1>{dashToTitle(ai_application_name)}</h1>
                    <LoginStatusWidget 
                        userInfo={userInfo} 
                        onLogout={handleLogout}
                        ai_application_url={ai_application_url}
                    />
                    {isAuthenticated() && (
                        <AssignmentTabs
                            problems={problems}
                            selectedTab={selectedTab}
                            onAssignmentTabClick={onAssignmentTabClick}
                        />
                    )}
                </header>

                <Routes>
                    <Route 
                        path="/login" 
                        element={
                            isAuthenticated() ? 
                                <Navigate to="/" /> : 
                                <LoginScreen
                                    onLoginSuccess={handleLoginSuccess}
                                    ai_application_url={ai_application_url}
                                />
                        } 
                    />
                    <Route
                       path="/" 
                       element={
                            false ? (
                                <Navigate to="/login" /> 
                            ) : (
                                <div className="three-column-layout">
                                    {/* Left Column - Control Panel */}
                                    <div className="column control-panel">
                                        <div className="widget-container">
                                            <InstructionsWidget
                                                problem={problems[selectedTab]}
                                            />
                                        </div>
                                        <div className="widget-container">
                                            <ConfigurationWidget
                                                config={config}
                                                handleInputChange={handleConfigurationInputChange}
                                            />
                                        </div>
                                    </div>

                                    {/* Middle Column - AI Panel */}
                                    <div className="column ai-panel">
                                        <div className="widget-container">

                                            <AIAssistantWidget
                                                endpoint={endpoint}
                                                languageModel={languageModel}
                                                temperature={llmTemperature}
                                                problem={problems[selectedTab]}
                                                config={config}
                                                userInfo={userInfo}
                                                problemDetails={problemDetails}
                                                handleAddResponseToArchivement={handleAddResponseToArchive}
                                            />
                                        </div>
                                    </div>

                                    {/* Right Column - Submission Panel */}
                                    <div className="column submission-panel">
                                        <div className="widget-container">
                                            <ResponseArchiveWidget 
                                                problem={problems[selectedTab]}
                                                savedResponses={savedResponses}
                                                selectedProblemId={problemDetails.problem_id}
                                                handleChangeSelectForSubmission={handleChangeSelectForSubmission}
                                            />
                                        </div>
                                    </div>
                                </div>
                            )
                       }
                    />
                </Routes>
            </div>
        </Router>



    );
}

export default App;
