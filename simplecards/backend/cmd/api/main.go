package main

import (
	"context"
	"log"
	"time"

	"simplecards/backend/internal/config"
	"simplecards/backend/internal/db"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	pool, err := db.New(cfg)
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}
	defer pool.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	var now time.Time
	err = pool.QueryRow(ctx, "SELECT NOW()").Scan(&now)
	if err != nil {
		log.Fatalf("query failed: %v", err)
	}

	log.Println("database pool connected successfully")
	log.Println("database time:", now)
}
