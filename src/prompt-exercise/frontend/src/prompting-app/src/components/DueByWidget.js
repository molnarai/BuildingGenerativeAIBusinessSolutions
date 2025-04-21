import React, { useState, useEffect } from 'react';

const DueByWidget = () => {
    const [timeRemaining, setTimeRemaining] = useState('');
    // const dueDate = new Date('2025-02-17T23:59:00');
    const dueDate = new Date('2025-04-26T23:59:00');

    useEffect(() => {
        const updateTimeRemaining = () => {
            const now = new Date();
            const diff = dueDate - now;

            // If the due date has passed
            if (diff < 0) {
                setTimeRemaining('Assignment is closed');
                return;
            }

            // Calculate time components
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

            // Format the message based on remaining time
            if (days >= 3) {
                setTimeRemaining('Due on April 26, 2025 before midnight');
            } else if (days > 0) {
                setTimeRemaining(`Due in ${days} day${days > 1 ? 's' : ''} and ${hours} hour${hours !== 1 ? 's' : ''}`);
            } else {
                setTimeRemaining(`Due in ${hours} hour${hours !== 1 ? 's' : ''} and ${minutes} minute${minutes !== 1 ? 's' : ''}`);
            }
        };

        // Update immediately and then every minute
        updateTimeRemaining();
        const interval = setInterval(updateTimeRemaining, 60000);

        // Cleanup interval on component unmount
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="due-by-widget">
            <span>{timeRemaining}</span>
        </div>
    );
};

export default DueByWidget;
