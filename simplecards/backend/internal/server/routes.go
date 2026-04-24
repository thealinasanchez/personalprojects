package server

import "simplecards/backend/internal/modules/users"

func (s *Server) registerRoutes() {
	s.mux.HandleFunc("/api/v1/health", s.healthHandler)

	usersHandler := users.NewHandler()
	usersHandler.RegisterRoutes(s.mux)
}
