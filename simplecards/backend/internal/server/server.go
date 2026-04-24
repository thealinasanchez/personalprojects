package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"

	"simplecards/backend/internal/config"
	"simplecards/backend/internal/middleware"
)

type Server struct {
	cfg  config.Config
	db   *pgxpool.Pool
	mux  *http.ServeMux
	http *http.Server
}

func New(cfg config.Config, db *pgxpool.Pool) *Server {
	mux := http.NewServeMux()

	s := &Server{
		cfg: cfg,
		db:  db,
		mux: mux,
	}

	s.registerRoutes()

	handler := middleware.SecurityHeaders(http.HandlerFunc(s.notFoundHandler))

	s.http = &http.Server{
		Addr:         ":8080",
		Handler:      handler,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  30 * time.Second,
	}

	return s
}

func (s *Server) Start() error {
	log.Printf("server starting on %s", s.http.Addr)
	return s.http.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	log.Println("server shutting down")

	if err := s.http.Shutdown(ctx); err != nil {
		return fmt.Errorf("shutdown server: %w", err)
	}

	log.Println("closing database pool")
	s.db.Close()

	return nil
}
