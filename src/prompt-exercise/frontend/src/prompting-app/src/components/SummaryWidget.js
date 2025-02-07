import React, { useState, useEffect } from "react";
import { useAuth } from "../AuthProvider";

const SummaryWidget = ({ completionCount, onRefresh, selectedTab }) => {

    const calculatePercentage = (selected, required) => {
        if (required === 0) return '0%';
        const percentage = Math.min((selected / required) * 100, 100);
        return `${Math.floor(percentage)}%`;
    };

    // Calculate totals
    const calculateTotals = () => {
        if (!completionCount || completionCount.length === 0) return null;
        
        return completionCount.reduce((acc, count) => ({
            selected_count: acc.selected_count + count.selected_count,
            total_count: acc.total_count + count.total_count,
            required_count: acc.required_count + count.required_count
        }), { selected_count: 0, total_count: 0, required_count: 0 });
    };

    const totals = calculateTotals();

    let summary_row_counter = 0;

    return (
        <div className="summary-widget">
            <div className="summary-header">
                <h3>Completion Summary</h3>
                <button 
                    onClick={onRefresh}
                    className="refresh-button"
                >
                   &#x21BB; Reload
                </button>
            </div>
            <div className="summary-content">
                {!completionCount || completionCount.length === 0 ? (
                    <p>No completion data available</p>
                ) : (
                    <div >
                        <table className="completion-stats">
                            <thead>
                                <tr>
                                    <th>Problem</th>
                                    <th>Completion</th>
                                    <th>Selected</th> 
                                    <th>Total</th>
                                    <th>Required</th>
                                </tr>
                            </thead>
                            <tbody>
                                {completionCount.map((count) => (
                                    <tr key={count.problem_id}
                                        className={summary_row_counter === selectedTab ? "stat-item-bold" : "stat-item"}>
                                        <td><span className="completion-stats-title">{`${++summary_row_counter}. ${count.problem_title}`}</span></td>
                                        <td><span className="count-value">{calculatePercentage(count.selected_count, count.required_count)}</span></td>
                                        <td><span className="count-value">{count.selected_count}</span></td>
                                        <td><span className="count-value">{count.total_count}</span></td>
                                        <td><span className="count-value">{count.required_count}</span></td>
                                    </tr>
                                ))}
                                {totals && (
                                    <tr className="totals-row">
                                        <td><strong>Totals</strong></td>
                                        <td>{calculatePercentage(totals.selected_count, totals.required_count)}</td>
                                        <td><strong>{totals.selected_count}</strong></td>
                                        <td><strong>{totals.total_count}</strong></td>
                                        <td><strong>{totals.required_count}</strong></td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                        <label>
                            <button
                                style={{ minWidth: "120px", marginTop: "20px" }}
                                className="submit-grading-button">
                                Submit for Homework
                            </button>
                        </label>
                    </div>
                   
                )}
            </div>
        </div>
    );
};


export default SummaryWidget;
