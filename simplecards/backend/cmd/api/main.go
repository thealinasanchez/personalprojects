package main

import (
	"context" // Handleas timeouts, cancellation, and request lifecycles
	"fmt"     // Used for formatting strings
	"log"     // For logging messages/errors to the console
	"os"      // Lets you access environment variables
	"time"    // Used for setting timeouts

	"github.com/jackc/pgx/v5" // PostgreSQL driver for GO
	"github.com/joho/godotenv"// Loads variables from a .env file
)

func main() {

	// Load environment variables from .env file into the system
	err := godotenv.Load()
	if err != nil {
		// If no .env file exists, it won't crash and will log a message
		log.Println(".env file not found, using system environment variables")
	}

	// Build the database connection string (DSN)
	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		os.Getenv("DB_HOST"),		// Get these from environment
		os.Getenv("DB_PORT"),
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASSWORD"),
		os.Getenv("DB_NAME"),
		os.Getenv("DB_SSLMODE"),
	)
	
	// Create a context wiht a timeout of 5 seconds
	// This prevents the app from hanging forever if DB connection fails
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	// means: run cancel() when this function exits
	
	// Connect to PostgreSQL using the connection string
	conn, err := pgx.Connect(ctx, dsn)
	if err != nil {
		log.Fatalf("unable to connect to database: %v", err)
	}
	defer conn.Close(ctx)
	
	// Test the connection by running a simple query
	var now time.Time
	err = conn.QueryRow(ctx, "SELECT NOW()").Scan(&now)
	if err != nil {
		log.Fatalf("query failed: %v", err)
	}

	log.Println("database connected successfully")
	log.Println("database time:", now)
}
