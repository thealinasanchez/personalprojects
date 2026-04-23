package main

import (
	"log"

	"simplecards/backend/internal/config"
	"simplecards/backend/internal/db"
	"simplecards/backend/internal/server"
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

	srv := server.New(cfg, pool)

	if err := srv.Start(); err != nil {
		log.Fatalf("server failed: %v", err)
	}
}
