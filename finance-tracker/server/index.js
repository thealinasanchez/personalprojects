/*
This is the primary entry point for the backend. It launches the HTTP
server, applies middleware, and exposes the initial health-check
endpoint.
*/

//1. MODULE IMPORTS

// Express creates the API server and set up route handlers
const express = require('express');

// CORS (Cross-Origin Resource Sharing) permits client browsers to call
// this server
const cors = require('cors');

// Import the database connection pool created in db.js
const pool = require('./db');

// Ensure environment variables are accessible
require('dotenv').config();

// 2. SERVER INITIALIZATION & MIDDLEWARE
const app = express();

// Use port 5000 by default, or fallback to an environment-assigned port
const PORT = process.env.PORT || 5000;

// Enable CORS so the React app running on another port can fetch data
// without being blocked
app.use(cors());

// Express middleware that parses incoming JSON request bodies (e.g.
// from POST requests)
app.use(express.json());

// 3. ROUTE HANDLERS

/*
* GET /api/health
* Verification endpoint to confirm that both the Node.js server
* and the Neon PostgreSQL database connection are functioning properly.
*/
app.get('/api/health', async (req, res) => {
    try {
        // Run a query on Neon to count the rows in the categories table
        const result = await pool.query('SELECT count(*) FROM categories;');
        
        // If query succeeds, return HTTP 200 with the count
        // (should be 10)
        res.status(200).json({
            status: 'ok',
            message: 'Server and Database connected successfully!',
            categoriesCount: result.rows[0].count
        });
    } catch (err) {
        // Log the error in the server console for debugging
        console.error('Database connection error:', err);

        // Send back an HTTP 500 response with the error details
        res.status(500).json({
            status: 'error', 
            message: 'Failed to query database',
            error: err.message
        });
    }
});

// 4. START THE SERVER

// Tell the application to start listening for incoming requests
// on the specified port
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
})