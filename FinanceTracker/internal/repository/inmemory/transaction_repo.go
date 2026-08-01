package inmemory

import (
    "context"
    "sync"
    "github.com/inxrius/FinanceTracker/internal/domain"
)

type TransactionRepository struct {
    mu           sync.RWMutex
    transactions map[int]*domain.Transaction
    nextID       int
}

func NewTransactionRepository() *TransactionRepository {
    return &TransactionRepository{
        transactions: make(map[int]*domain.Transaction),
        nextID: 1,
    }
}

func (r *TransactionRepository) Create(_ context.Context, tx *domain.Transaction) error {
    r.mu.Lock()
    defer r.mu.Unlock()
    tx.ID = r.nextID
    r.nextID++
    r.transactions[tx.ID] = tx
    return nil
}

func (r *TransactionRepository) GetByID(_ context.Context, id int) (*domain.Transaction, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    tx, ok := r.transactions[id]
    if !ok {
        return nil, domain.ErrTransactionNotFound
    }
    return tx, nil
}

func (r *TransactionRepository) GetAllByUser(_ context.Context, userID int) ([]domain.Transaction, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    var result []domain.Transaction
    for _, tx := range r.transactions {
        if tx.UserID == userID {
            result = append(result, *tx)
        }
    }
    return result, nil
}

func (r *TransactionRepository) GetAll(_ context.Context) ([]domain.Transaction, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	var result []domain.Transaction
	for _, tx := range r.transactions {
		result = append(result, *tx)
	}
	return result, nil
}