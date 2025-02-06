import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../AuthProvider';
// import { useNavigate } from 'react-router-dom';
// import { Box, Typography, CircularProgress } from '@mui/material';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';


export const SyncResponseWidget = ({ queuedResponses, ai_application_url, onResponsesSaved }) => {
  const [isSyncing, setIsSyncing] = useState(false);
  const [error, setError] = useState(null);
  const { accessToken } = useAuth();
  
  // Function to save a single response
  const saveResponse = async (response) => {
    try {
      const result = await fetch(`${ai_application_url}/assignment/responses/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(response),
      });

      const data = await result.json();
      
      if (!data.success) {
        throw new Error(data.message);
      }

      return { success: true, response };
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save response');
      return { success: false, response };
    }
  };

  // Function to process all queued responses
  const processQueue = useCallback(async () => {
    if (queuedResponses.length === 0 || isSyncing) return;

    setIsSyncing(true);
    setError(null);

    try {
      // Process all responses in parallel
      const results = await Promise.all(
        queuedResponses.map(response => saveResponse(response))
      );

      // Separate successful and failed responses
      const successfulResponses = results
        .filter(result => result.success)
        .map(result => result.response);

      // Remove successful responses from the queue
      if (successfulResponses.length > 0) {
        onResponsesSaved(successfulResponses);
      }

      // Check if any saves failed
      const hasFailures = results.some(result => !result);
      if (hasFailures) {
        setError('Some responses failed to sync');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process queue');
    } finally {
      setIsSyncing(false);
    }
  }, [queuedResponses, isSyncing, onResponsesSaved]);

  // Effect to process queue when queuedResponses changes
  useEffect(() => {
    processQueue();
  }, [queuedResponses]); // processQueue is intentionally omitted to prevent recursive triggers

  // Effect to check queue periodically
  useEffect(() => {
    const interval = setInterval(() => {
      if (queuedResponses.length > 0) {
        processQueue();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [queuedResponses.length]); // processQueue is intentionally omitted

  return (
    <Box
      sx={{
        p: 2,
        border: '1px solid',
        borderColor: error ? 'error.main' : 'divider',
        borderRadius: 1,
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        fontSize: 'small',
      }}
    >
      {isSyncing && <CircularProgress size={20} />}
      <Typography color="info" fontSize="0.875rem">
        {queuedResponses.length == 0 ? "All in sync" : `${queuedResponses.length} pending response${queuedResponses.length !== 1 ? 's' : ''} to sync`}
      </Typography>
      {error && (
        <Typography color="error" fontSize="0.875rem">
          {error}
        </Typography>
      )}
    </Box>
  );
};
