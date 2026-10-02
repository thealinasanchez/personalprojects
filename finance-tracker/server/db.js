/*
This module manages the connection pool to your cloud database. Rather
than opening & closing a separate network connection for every single
query, a Pool maintains a cache of reusable database connections.
*/

// 1. Import the Pool object from the PostgreSQL library ('pg')
const { Pool } = require('pg');

// 1. Load environment variables from the server/.env file 
//    into process.env
require('dotenv').config();

// 3. Create a connection pool configured with your Neon credentials
const pool = new Pool({
    // Read the secret database URI from .env file
    connectionString: process.env.DATABASE_URL,

    // Cloud providers like Neon require secure SSL/TLS encryption for
    // database queries.
    // rejectUnauthorized: false prevents errors regarding self-signed
    // certificate chains.
    ssl: {
        rejectUnauthorized: false
    }
});

// 4. Export the pool instance so other server files (like index.js)
//    can run database queries
module.exports = pool;