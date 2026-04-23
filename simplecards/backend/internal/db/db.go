package db

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5"

	"simplecards/backend/internal/config"
)

func New(cfg config.Config) (*pgx.Conn, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	conn, err := pgx.Connect(ctx, cfg.DBConnString())
	if err != nil {
		return nil, fmt.Errorf("connect to database: %w", err)
	}

	return conn, nil
}
