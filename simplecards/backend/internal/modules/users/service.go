package users

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

func (s *Service) LoginUser(ctx context.Context, req loginUserRequest) (loginUserResponse, error) {
	userWithHash, err := s.repo.GetUserByEmail(ctx, req.Email)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			return loginUserResponse{}, ErrInvalidCredentials
		}

		return loginUserResponse{}, err
	}

	if err := bcrypt.CompareHashAndPassword([]byte(userWithHash.PasswordHash), []byte(req.Password)); err != nil {
		return loginUserResponse{}, ErrInvalidCredentials
	}

	user := userResponse{
		ID:        userWithHash.ID,
		Email:     userWithHash.Email,
		Username:  userWithHash.Username,
		CreatedAt: userWithHash.CreatedAt,
	}

	token, err := s.generateToken(user)
	if err != nil {
		return loginUserResponse{}, err
	}

	return loginUserResponse{
		User:  user,
		Token: token,
	}, nil
}

func (s *Service) generateToken(user userResponse) (string, error) {
	claims := jwt.MapClaims{
		"user_id":  user.ID,
		"email":    user.Email,
		"username": user.Username,
		"exp":      time.Now().Add(24 * time.Hour).Unix(),
		"iat":      time.Now().Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	signedToken, err := token.SignedString([]byte(s.jwtSecret))
	if err != nil {
		return "", fmt.Errorf("sign jwt token: %w", err)
	}

	return signedToken, nil
}
