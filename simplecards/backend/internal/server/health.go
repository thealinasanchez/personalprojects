package server

import "net/http"

type healthResponse struct {
	Status string `json:"status"`
}

func (s *Server) healthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{
			"error": "method not allowed",
		})
		return
	}

	writeJSON(w, http.StatusOK, healthResponse{
		Status: "ok",
	})
}
