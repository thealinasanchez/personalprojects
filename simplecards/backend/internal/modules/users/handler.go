package users

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Handler struct {
	service *Service
}

func NewHandler(db *pgxpool.Pool) *Handler {
	repo := NewRepository(db)
	service := NewService(repo)

	return &Handler{
		service: service,
	}
}

func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/api/v1/users", h.handleUsers)
	mux.HandleFunc("/api/v1/users/", h.handleUserByID)
}

func (h *Handler) handleUsers(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		h.listUsers(w, r)
	case http.MethodPost:
		h.createUser(w, r)
	default:
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
	}
}

func (h *Handler) handleUserByID(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	id := strings.TrimPrefix(r.URL.Path, "/api/v1/users/")
	id = strings.TrimSpace(id)

	if id == "" {
		writeError(w, http.StatusBadRequest, "user id is required")
		return
	}

	if strings.Contains(id, "/") {
		writeError(w, http.StatusNotFound, "route not found")
		return
	}

	if err := validateUserID(id); err != nil {
		writeError(w, http.StatusBadRequest, "invalid user id")
		return
	}

	user, err := h.service.GetUserByID(r.Context(), id)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			writeError(w, http.StatusNotFound, "user not found")
			return
		}

		writeError(w, http.StatusInternalServerError, "failed to fetch user")
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"user": user,
	})
}

func (h *Handler) listUsers(w http.ResponseWriter, r *http.Request) {
	users, err := h.service.ListUsers(r.Context())
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to fetch users")
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"users": users,
	})
}

func (h *Handler) createUser(w http.ResponseWriter, r *http.Request) {
	var req createUserRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid json body")
		return
	}

	req = normalizeCreateUserRequest(req)

	if err := validateCreateUserRequest(req); err != nil {
		writeError(w, http.StatusBadRequest, err.Error())
		return
	}

	user, err := h.service.CreateUser(r.Context(), req)
	if err != nil {
		if errors.Is(err, ErrUserAlreadyExists) {
			writeError(w, http.StatusConflict, "email or username already exists")
			return
		}

		writeError(w, http.StatusInternalServerError, "failed to create user")
		return
	}

	writeJSON(w, http.StatusCreated, map[string]any{
		"user": user,
	})
}
