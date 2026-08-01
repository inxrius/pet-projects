package service

import (
	"fmt"
	"context"
	"github.com/inxrius/FinanceTracker/internal/repository"
	"github.com/inxrius/FinanceTracker/internal/domain"
)

type UserService struct {
	userRepo repository.UserRepository
}

func NewUserService(userRepo repository.UserRepository) *UserService {
	return &UserService{userRepo}
}

func (s *UserService) Register(ctx context.Context, name, email string) (*domain.User, error) {
	user, err := domain.NewUser(name, email)
	if err != nil {
		return nil, fmt.Errorf("UserService.Register: %w", err)
	}
	err = s.userRepo.Create(ctx, user)
	if err != nil {
		return nil, fmt.Errorf("UserService.Register: %w", err)
	}
	return user, nil
}

func (s *UserService) GetUser(ctx context.Context, id int) (*domain.User, error) {
	user, err := s.userRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("UserService.GetUser: %w", err)
	}
	return user, nil
}

func (s *UserService) GetAllUsers (ctx context.Context) ([]domain.User, error) {
	users, err := s.userRepo.GetAll(ctx)
	if err != nil {
		return nil, fmt.Errorf("UserService.GetAllUsers: %w", err)
	}
	return users, nil
}