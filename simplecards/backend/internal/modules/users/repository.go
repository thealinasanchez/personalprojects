package users

import (
	"context"
	"errors"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

var ErrUserNotFound = errors.New("user not found")
var ErrUserAlreadyExists = errors.New("user already exists")

type Repository struct {
	db *pgxpool.Pool
}

func NewRepository(db *pgxpool.Pool) *Repository {
	return &Repository{
		db: db,
	}
}

func (r *Repository) ListUsers(ctx context.Context) ([]userResponse, error) {
	rows, err := r.db.Query(
		ctx,
		`
		SELECT id::text, email, username, created_at::text
		FROM users
		ORDER BY created_at DESC
		LIMIT 20
		`,
	)
	if err != nil {
		return nil, fmt.Errorf("query users: %w", err)
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
			return nil, fmt.Errorf("scan user row: %w", err)
		}

		users = append(users, user)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("read user rows: %w", err)
	}

	return users, nil
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

func (r *Repository) CreateUser(ctx context.Context, params createUserParams) (userResponse, error) {
	var user userResponse

	err := r.db.QueryRow(
		ctx,
		`
		INSERT INTO users (email, username, password_hash)
		VALUES ($1, $2, $3)
		RETURNING id::text, email, username, created_at::text
		`,
		params.Email,
		params.Username,
		params.PasswordHash,
	).Scan(
		&user.ID,
		&user.Email,
		&user.Username,
		&user.CreatedAt,
	)

	if err != nil {
		var pgErr *pgconn.PgError

		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			return userResponse{}, ErrUserAlreadyExists
		}

		return userResponse{}, fmt.Errorf("insert user: %w", err)
	}

	return user, nil
}
