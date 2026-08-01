package inmemory

import (
    "context"
    "sync"
    "github.com/inxrius/FinanceTracker/internal/domain"
)

type UserRepository struct {
    mu    sync.RWMutex
    users map[int]*domain.User
    nextID int
}

func NewUserRepository() *UserRepository {
    return &UserRepository{
        users: make(map[int]*domain.User),
        nextID: 1,
    }
}

func (r *UserRepository) Create(_ context.Context, user *domain.User) error {
    r.mu.Lock()
    defer r.mu.Unlock()
    user.ID = r.nextID
    r.nextID++
    r.users[user.ID] = user
    return nil
}

func (r *UserRepository) GetByID(_ context.Context, id int) (*domain.User, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    user, ok := r.users[id]
    if !ok {
        return nil, domain.ErrUserNotFound
    }
    return user, nil
}

func (r *UserRepository) GetAll(_ context.Context) ([]domain.User, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    result := make([]domain.User, 0, len(r.users))
    for _, u := range r.users {
        result = append(result, *u)
    }
    return result, nil
}