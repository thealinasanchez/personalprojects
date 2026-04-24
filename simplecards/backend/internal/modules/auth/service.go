package auth

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

var ErrInvalidCredentials = errors.New("invalid email or password")

type Service struct {
	repo      *Repository
	jwtSecret string
}

func NewService(repo *Repository, jwtSecret string) *Service {
	return &Service{
		repo:      repo,
		jwtSecret: jwtSecret,
	}
}

func (s *Service) Login(ctx context.Context, req loginRequest) (loginResponse, error) {
	userWithHash, err := s.repo.GetUserByEmail(ctx, req.Email)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			return loginResponse{}, ErrInvalidCredentials
		}

		return loginResponse{}, err
	}

	if err := bcrypt.CompareHashAndPassword([]byte(userWithHash.PasswordHash), []byte(req.Password)); err != nil {
		return loginResponse{}, ErrInvalidCredentials
	}

	user := userResponse{
		ID:        userWithHash.ID,
		Email:     userWithHash.Email,
		Username:  userWithHash.Username,
		CreatedAt: userWithHash.CreatedAt,
	}

	token, err := s.generateToken(user)
	if err != nil {
		return loginResponse{}, err
	}

	return loginResponse{
		User:  user,
		Token: token,
	}, nil
}

func (s *Service) GetCurrentUser(ctx context.Context, userID string) (userResponse, error) {
	return s.repo.GetUserByID(ctx, userID)
}

func (s *Service) generateToken(user userResponse) (string, error) {
	now := time.Now()

	claims := jwt.MapClaims{
		"user_id":  user.ID,
		"email":    user.Email,
		"username": user.Username,
		"exp":      now.Add(24 * time.Hour).Unix(),
		"iat":      now.Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	signedToken, err := token.SignedString([]byte(s.jwtSecret))
	if err != nil {
		return "", fmt.Errorf("sign jwt token: %w", err)
	}

	return signedToken, nil
}
