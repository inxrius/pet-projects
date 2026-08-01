package inmemory

import (
    "context"
    "sync"
    "github.com/inxrius/FinanceTracker/internal/domain"
)

type CategoryRepository struct {
    mu       sync.RWMutex
    categories map[int]*domain.Category
    nextID   int
}

func NewCategoryRepository() *CategoryRepository {
    return &CategoryRepository{
        categories: make(map[int]*domain.Category),
        nextID: 1,
    }
}

func (r *CategoryRepository) Create(_ context.Context, cat *domain.Category) error {
    r.mu.Lock()
    defer r.mu.Unlock()
    cat.ID = r.nextID
    r.nextID++
    r.categories[cat.ID] = cat
    return nil
}

func (r *CategoryRepository) GetByID(_ context.Context, id int) (*domain.Category, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    cat, ok := r.categories[id]
    if !ok {
        return nil, domain.ErrCategoryNotFound
    }
    return cat, nil
}

func (r *CategoryRepository) GetAllByUser(_ context.Context, userID int) ([]domain.Category, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    var result []domain.Category
    for _, c := range r.categories {
        if c.UserID == userID {
            result = append(result, *c)
        }
    }
    return result, nil
}

func (r *CategoryRepository) Delete(_ context.Context, id int) error {
    r.mu.Lock()
    defer r.mu.Unlock()
    if _, ok := r.categories[id]; !ok {
        return domain.ErrCategoryNotFound
    }
    delete(r.categories, id)
    return nil
}