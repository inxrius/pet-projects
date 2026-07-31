package repository

import (
    "context"
    "github.com/inxrius/FinanceTracker/internal/domain"
)

type TransactionRepository interface {
    Create(ctx context.Context, transaction *domain.Transaction) error
    GetByID(ctx context.Context, id int) (*domain.Transaction, error)
    GetAllByUser(ctx context.Context, userID int) ([]domain.Transaction, error)
}