package users

import (
	"context"
	"errors"
	"fmt"

	"golang.org/x/crypto/bcrypt"
)

var ErrInvalidCredentials = errors.New("invalid email or password")

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

func (s *Service) GetUserByEmail(ctx context.Context, email string) (userWithPasswordHash, error) {
	return s.repo.GetUserByEmail(ctx, email)
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

func (s *Service) LoginUser(ctx context.Context, req loginUserRequest) (userResponse, error) {
	userWithHash, err := s.repo.GetUserByEmail(ctx, req.Email)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			return userResponse{}, ErrInvalidCredentials
		}

		return userResponse{}, err
	}

	if err := bcrypt.CompareHashAndPassword([]byte(userWithHash.PasswordHash), []byte(req.Password)); err != nil {
		return userResponse{}, ErrInvalidCredentials
	}

	return userResponse{
		ID:        userWithHash.ID,
		Email:     userWithHash.Email,
		Username:  userWithHash.Username,
		CreatedAt: userWithHash.CreatedAt,
	}, nil
}
