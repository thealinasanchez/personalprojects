package server

import (
	"net/http"
	"strings"
)

func (s *Server) notFoundHandler(w http.ResponseWriter, r *http.Request) {
	knownRoutes := []string{
		"/api/v1/health",
		"/api/v1/users",
		"/api/v1/users/",
		"/api/v1/auth/login",
		"/api/v1/auth/me",
	}

	for _, route := range knownRoutes {
		if r.URL.Path == route || strings.HasPrefix(r.URL.Path, route) && strings.HasSuffix(route, "/") {
			s.mux.ServeHTTP(w, r)
			return
		}
	}

	writeJSON(w, http.StatusNotFound, map[string]string{
		"error": "route not found",
	})
}
