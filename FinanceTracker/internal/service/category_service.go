package service

import (
	"fmt"
	"context"
	"github.com/inxrius/FinanceTracker/internal/domain"
	"github.com/inxrius/FinanceTracker/internal/repository"
)

type CategoryService struct {
	categoryRepo    repository.CategoryRepository
	transactionRepo repository.TransactionRepository
}

func NewCategoryService(
	categoryRepo repository.CategoryRepository,
	transactionRepo repository.TransactionRepository,
) *CategoryService {
	return &CategoryService{categoryRepo, transactionRepo}
}

func (s *CategoryService) CreateCategory(ctx context.Context, userID int, name, categoryType string) (*domain.Category, error) {
	category, err := domain.NewCategory(userID, name, categoryType)
	if err != nil {
		return nil, fmt.Errorf("CategoryService.CreateCategory: %w", err)
	}
	err = s.categoryRepo.Create(ctx, category)
	if err != nil {
		return nil, fmt.Errorf("CategoryService.CreateCategory: %w", err)
	}
	return category, nil
}

func (s *CategoryService) GetCategoryByID(ctx context.Context, id int) (*domain.Category, error) {
	category, err := s.categoryRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("CategoryService.GetCategoryByID: %w", err)
	}
	return category, nil
}

func (s *CategoryService) GetUserCategories(ctx context.Context, userID int) ([]domain.Category, error) {
	categories, err := s.categoryRepo.GetAllByUser(ctx, userID)
	if err != nil {
		return nil, fmt.Errorf("CategoryService.GetUserCategories: %w", err)
	}
	return categories, nil
}

func (s *CategoryService) DeleteCategory(ctx context.Context, id int) error {
	transactions, err := s.transactionRepo.GetAll(ctx)
	if err != nil {
		return fmt.Errorf("CategoryService.DeleteCategory: %w", err)
	}
	for _, tx := range transactions {
		if tx.CategoryID == id {
			return fmt.Errorf("CategoryService.DeleteCategory: %w", domain.ErrCategoryHasTransactions)
		}
	}
	err = s.categoryRepo.Delete(ctx, id)
	if err != nil {
		return fmt.Errorf("CategoryService.DeleteCategory: %w", err)
	}
	return nil
}