package server

func (s *Server) registerRoutes() {
	s.mux.HandleFunc("/api/v1/health", s.healthHandler)
}
