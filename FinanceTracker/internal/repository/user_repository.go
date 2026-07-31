package repository

import (
    "context"
    "github.com/inxrius/FinanceTracker/internal/domain"
)

type UserRepository interface {
    Create(ctx context.Context, user *domain.User) error
    GetByID(ctx context.Context, id int) (*domain.User, error)
    GetAll(ctx context.Context) ([]domain.User, error)
}