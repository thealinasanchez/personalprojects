package users

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Handler struct {
	db *pgxpool.Pool
}

func NewHandler(db *pgxpool.Pool) *Handler {
	return &Handler{
		db: db,
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
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{
			"error": "method not allowed",
		})
	}
}

func (h *Handler) handleUserByID(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{
			"error": "method not allowed",
		})
		return
	}

	id := strings.TrimPrefix(r.URL.Path, "/api/v1/users/")
	id = strings.TrimSpace(id)

	if id == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": "user id is required",
		})
		return
	}

	var user userResponse

	err := h.db.QueryRow(
		r.Context(),
		`
		SELECT id::text, email, username, created_at::text
		FROM users
		WHERE id = $1
		`,
		id,
	).Scan(
		&user.ID,
		&user.Email,
		&user.Username,
		&user.CreatedAt,
	)

	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			writeJSON(w, http.StatusNotFound, map[string]string{
				"error": "user not found",
			})
			return
		}

		writeJSON(w, http.StatusInternalServerError, map[string]string{
			"error": "failed to fetch user",
		})
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"user": user,
	})
}

func (h *Handler) listUsers(w http.ResponseWriter, r *http.Request) {
	rows, err := h.db.Query(
		r.Context(),
		`
		SELECT id::text, email, username, created_at::text
		FROM users
		ORDER BY created_at DESC
		LIMIT 20
		`,
	)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{
			"error": "failed to fetch users",
		})
		return
	}
	defer rows.Close()

	users := []userResponse{}

	for rows.Next() {
		var user userResponse

		if err := rows.Scan(
			&user.ID,
			&user.Email,
			&user.Username,
			&user.CreatedAt,
		); err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{
				"error": "failed to read user row",
			})
			return
		}

		users = append(users, user)
	}

	if err := rows.Err(); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{
			"error": "failed while reading users",
		})
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"users": users,
	})
}

func (h *Handler) createUser(w http.ResponseWriter, r *http.Request) {
	var req createUserRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": "invalid json body",
		})
		return
	}

	req.Email = strings.TrimSpace(req.Email)
	req.Username = strings.TrimSpace(req.Username)
	req.PasswordHash = strings.TrimSpace(req.PasswordHash)

	if req.Email == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": "email is required",
		})
		return
	}

	if req.Username == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": "username is required",
		})
		return
	}

	if req.PasswordHash == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": "password_hash is required",
		})
		return
	}

	var user userResponse

	err := h.db.QueryRow(
		r.Context(),
		`
		INSERT INTO users (email, username, password_hash)
		VALUES ($1, $2, $3)
		RETURNING id::text, email, username, created_at::text
		`,
		req.Email,
		req.Username,
		req.PasswordHash,
	).Scan(
		&user.ID,
		&user.Email,
		&user.Username,
		&user.CreatedAt,
	)
	if err != nil {
		var pgErr *pgconn.PgError

		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			writeJSON(w, http.StatusConflict, map[string]string{
				"error": "email or username already exists",
			})
			return
		}

		writeJSON(w, http.StatusInternalServerError, map[string]string{
			"error": "failed to create user",
		})
		return
	}

	writeJSON(w, http.StatusCreated, map[string]any{
		"user": user,
	})
}
