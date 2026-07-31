package repository

import (
    "context"
    "github.com/inxrius/FinanceTracker/internal/domain"
)

type CategoryRepository interface {
    Create(ctx context.Context, category *domain.Category) error
    GetByID(ctx context.Context, id int) (*domain.Category, error)
    GetAllByUser(ctx context.Context, userID int) ([]domain.Category, error)
    Delete(ctx context.Context, id int) error
}