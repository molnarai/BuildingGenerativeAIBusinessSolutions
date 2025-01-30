import React, { useState, useEffect } from "react";

const AssignmentTabs = ({ problems, selectedTab, onAssignmentTabClick }) => {
  // const [problems, setProblems] = useState([]);
  // const [selectedTab, setSelectedTab] = useState(0); // Default to the first tab

  // // Fetch problems from the API
  // useEffect(() => {
  //   const fetchProblems = async () => {
  //     try {
  //       const response = await fetch("http://localhost:8000/assignment/problems");
  //       if (!response.ok) {
  //         throw new Error("Failed to fetch problems");
  //       }
  //       const data = await response.json();
  //       setProblems(data.problems);
  //     } catch (error) {
  //       console.error("Error fetching problems:", error);
  //     }
  //   };

  //   fetchProblems();
  // }, []);

  // // Handle tab selection
  // const onAssignmentTabClick = (index) => {
  //   setSelectedTab(index);
  // };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      {/* Tab Bar */}
      {/* <div style={{ display: "flex", borderBottom: "2px solid #ddd", marginBottom: "20px" }}> */}
      <div className="assignment-tabs">
        {problems.map((problem, index) => (
          <div
            key={problem.id}
            onClick={() => onAssignmentTabClick(index)}
            style={{
              padding: "10px 20px",
              cursor: "pointer",
              borderBottom: selectedTab === index ? "3px solid #007BFF" : "none",
              color: selectedTab === index ? "#007BFF" : "#555",
              fontWeight: selectedTab === index ? "bold" : "normal",
            }}
          >
            {index + 1}. {problem.title}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AssignmentTabs;
