package server

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"

	"simplecards/backend/internal/config"
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

	s.http = &http.Server{
		Addr:         ":8080",
		Handler:      s.mux,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  30 * time.Second,
	}

	return s
}

func (s *Server) registerRoutes() {
	s.mux.HandleFunc("/health", s.healthHandler)
}

func (s *Server) Start() error {
	log.Printf("server starting on %s", s.http.Addr)
	return s.http.ListenAndServe()
}

func (s *Server) healthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	_, _ = fmt.Fprintln(w, "ok")
}
