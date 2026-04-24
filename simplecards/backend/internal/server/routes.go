package server

import (
	"simplecards/backend/internal/modules/auth"
	"simplecards/backend/internal/modules/users"
)

func (s *Server) registerRoutes() {
	s.mux.HandleFunc("/api/v1/health", s.healthHandler)

	usersHandler := users.NewHandler(s.db)
	usersHandler.RegisterRoutes(s.mux)

	authHandler := auth.NewHandler(s.cfg, s.db)
	authHandler.RegisterRoutes(s.mux)
}
