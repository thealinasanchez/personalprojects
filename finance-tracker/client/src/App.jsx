// client/src/App.jsx

// 1. Import hooks from React:
// - useState: lets us store values that change over time and cause the screen to re-render
// - useEffect: lets us run side effects (like fetching data over the network) when the page loads
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  // -------------------------------------------------------------
  // State variables
  // -------------------------------------------------------------
  // healthData: stores the JSON response object from the backend
  const [healthData, setHealthData] = useState(null);
  // loading: boolean flag to show a "Loading..." message while fetching
  const [loading, setLoading] = useState(true);
  // error: stores an error message if the fetch fails
  const [error, setError] = useState(null);

  // -------------------------------------------------------------
  // Data Fetching
  // -------------------------------------------------------------
  // The empty array [] at the end means this function runs exactly once when the component first loads
  useEffect(() => {
    // Call the backend API running on port 5000
    fetch('http://localhost:5000/api/health')
      .then((response) => {
        // If server responds with an HTTP error code (404, 500, etc.), throw an error
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        // Parse the raw incoming response into a JavaScript object
        return response.json();
      })
      .then((data) => {
        // Store the parsed backend data in our state
        setHealthData(data);
        // Turn off the loading state since the request is finished
        setLoading(false);
      })
      .catch((err) => {
        // Log the error in the browser console for debugging
        console.error('Fetch error:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // -------------------------------------------------------------
  // UI Rendering
  // -------------------------------------------------------------
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Finance Tracker</h1>
      <h2>System Status Check</h2>

      {/* 1. Show message while waiting for the network response */}
      {loading && <p>Checking database connection...</p>}

      {/* 2. Display red alert if network or server failed */}
      {error && (
        <p style={{ color: 'red' }}>
          Failed to connect to backend: {error}
        </p>
      )}

      {/* 3. If data arrived successfully, display the database report */}
      {healthData && (
        <div style={{ 
          border: '1px solid #4CAF50', 
          borderRadius: '8px', 
          padding: '1rem', 
          backgroundColor: '#f9fff9',
          color: '#333'
        }}>
          <p><strong>Server Status:</strong> {healthData.status}</p>
          <p><strong>Message:</strong> {healthData.message}</p>
          <p><strong>Live Seeded Categories Count:</strong> {healthData.categoriesCount}</p>
        </div>
      )}
    </div>
  );
}

export default App;