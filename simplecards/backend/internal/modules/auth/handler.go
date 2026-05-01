package auth

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/jackc/pgx/v5/pgxpool"

	"simplecards/backend/internal/config"
	"simplecards/backend/internal/middleware"
)

type Handler struct {
	service *Service
	auth    *middleware.AuthMiddleware
}

func NewHandler(cfg config.Config, db *pgxpool.Pool) *Handler {
	repo := NewRepository(db)
	service := NewService(repo, cfg.JWTSecret)
	authMiddleware := middleware.NewAuthMiddleware(cfg.JWTSecret)

	return &Handler{
		service: service,
		auth:    authMiddleware,
	}
}

func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/api/v1/auth/login", h.handleLogin)
	mux.Handle("/api/v1/auth/me", h.auth.RequireAuth(http.HandlerFunc(h.handleMe)))
}

func (h *Handler) handleLogin(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	var req loginRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid json body")
		return
	}

	req = normalizeLoginRequest(req)

	if err := validateLoginRequest(req); err != nil {
		writeError(w, http.StatusBadRequest, err.Error())
		return
	}

	loginResponse, err := h.service.Login(r.Context(), req)
	if err != nil {
		if errors.Is(err, ErrInvalidCredentials) {
			writeError(w, http.StatusUnauthorized, "invalid email or password")
			return
		}

		writeError(w, http.StatusInternalServerError, "failed to login")
		return
	}

	writeJSON(w, http.StatusOK, loginResponse)
}

func (h *Handler) handleMe(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	userID := middleware.UserIDFromContext(r.Context())

	user, err := h.service.GetCurrentUser(r.Context(), userID)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			writeError(w, http.StatusNotFound, "user not found")
			return
		}

		writeError(w, http.StatusInternalServerError, "failed to fetch current user")
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"user": user,
	})
}
