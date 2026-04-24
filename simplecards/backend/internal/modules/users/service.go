package users

import (
	"context"
	"fmt"

	"golang.org/x/crypto/bcrypt"
)

type Service struct {
	repo *Repository
}

func NewService(repo *Repository) *Service {
	return &Service{
		repo: repo,
	}
}

func (s *Service) ListUsers(ctx context.Context) ([]userResponse, error) {
	return s.repo.ListUsers(ctx)
}

func (s *Service) GetUserByID(ctx context.Context, id string) (userResponse, error) {
	return s.repo.GetUserByID(ctx, id)
}

func (s *Service) CreateUser(ctx context.Context, req createUserRequest) (userResponse, error) {
	hashBytes, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return userResponse{}, fmt.Errorf("hash password: %w", err)
	}

	params := createUserParams{
		Email:        req.Email,
		Username:     req.Username,
		PasswordHash: string(hashBytes),
	}

	return s.repo.CreateUser(ctx, params)
}
