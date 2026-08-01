package service

import (
	"fmt"
	"time"
	"context"
	"github.com/inxrius/FinanceTracker/internal/domain"
	"github.com/inxrius/FinanceTracker/internal/repository"
)

type TransactionService struct {
	transactionRepo repository.TransactionRepository
	categoryRepo repository.CategoryRepository
}

func NewTransactionService(
	transactionRepo repository.TransactionRepository,
	categoryRepo repository.CategoryRepository,
) *TransactionService {
	return &TransactionService{transactionRepo, categoryRepo}
}

func (s *TransactionService) CreateTransaction(
	ctx context.Context,
	userID, categoryID int,
	amount float64,
	description string,
	date time.Time,
) (*domain.Transaction, error) {
	transaction, err := domain.NewTransaction(
		userID,
		categoryID,
		amount,
		description,
		date,
	)
	if err != nil {
		return nil, fmt.Errorf("TransactionService.CreateTransaction: %w", err)
	}
	category, err := s.categoryRepo.GetByID(ctx, categoryID)
	if err != nil {
		return nil, fmt.Errorf("TransactionService.CreateTransaction: %w", err)
	}
	if category.UserID != userID {
		return nil, fmt.Errorf("TransactionService.CreateTransaction: %w", domain.ErrCategoryDoesNotBelongToUser)
	}
	err = s.transactionRepo.Create(ctx, transaction)
	if err != nil {
		return nil, fmt.Errorf("TransactionService.CreateTransaction: %w", err)
	}
	return transaction, nil
}

func (s *TransactionService) GetUserTransactions(
	ctx context.Context,
	userID int,
) ([]domain.Transaction, error) {
	transactions, err := s.transactionRepo.GetAllByUser(ctx, userID)
	if err != nil {
		return nil, fmt.Errorf("TransactionService.GetUserTransactions: %w", err)
	}
	return transactions, nil
}