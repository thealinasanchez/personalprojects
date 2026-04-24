package users

import "context"

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
	return s.repo.CreateUser(ctx, req)
}
