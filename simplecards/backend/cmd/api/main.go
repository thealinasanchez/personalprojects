package main

import (
	"context"
	"log"
	"time"

	"github.com/jackc/pgx/v5"

	"simplecards/backend/internal/config"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	conn, err := pgx.Connect(ctx, cfg.DBConnString())
	if err != nil {
		log.Fatalf("unable to connect to database: %v", err)
	}
	defer conn.Close(ctx)

	var now time.Time
	err = conn.QueryRow(ctx, "SELECT NOW()").Scan(&now)
	if err != nil {
		log.Fatalf("query failed: %v", err)
	}

	log.Println("database connected successfully")
	log.Println("database time:", now)
}
