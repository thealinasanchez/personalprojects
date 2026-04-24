package auth

import (
	"context"
	"errors"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

var ErrUserNotFound = errors.New("user not found")

type Repository struct {
	db *pgxpool.Pool
}

func NewRepository(db *pgxpool.Pool) *Repository {
	return &Repository{
		db: db,
	}
}

func (r *Repository) GetUserByEmail(ctx context.Context, email string) (userWithPasswordHash, error) {
	var user userWithPasswordHash

	err := r.db.QueryRow(
		ctx,
		`
		SELECT id::text, email, username, password_hash, created_at::text
		FROM users
		WHERE email = $1
		`,
		email,
	).Scan(
		&user.ID,
		&user.Email,
		&user.Username,
		&user.PasswordHash,
		&user.CreatedAt,
	)

	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return userWithPasswordHash{}, ErrUserNotFound
		}

		return userWithPasswordHash{}, fmt.Errorf("query user by email: %w", err)
	}

	return user, nil
}

func (r *Repository) GetUserByID(ctx context.Context, id string) (userResponse, error) {
	var user userResponse

	err := r.db.QueryRow(
		ctx,
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
			return userResponse{}, ErrUserNotFound
		}

		return userResponse{}, fmt.Errorf("query user by id: %w", err)
	}

	return user, nil
}
