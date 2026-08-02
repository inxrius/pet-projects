package handler

import (
    "encoding/json"
    "errors"
    "net/http"
    "time"

    "github.com/inxrius/FinanceTracker/internal/domain"
    "github.com/inxrius/FinanceTracker/internal/service"
)

type TransactionHandler struct {
    transactionService *service.TransactionService
}

func NewTransactionHandler(transactionService *service.TransactionService) *TransactionHandler {
    return &TransactionHandler{transactionService: transactionService}
}

type CreateTransactionRequest struct {
    CategoryID  int     `json:"category_id"`
    Amount      float64 `json:"amount"`
    Description string  `json:"description"`
    Date        string  `json:"date"` // ожидаем формат "2006-01-02"
}

type TransactionResponse struct {
    ID          int     `json:"id"`
    UserID      int     `json:"user_id"`
    CategoryID  int     `json:"category_id"`
    Amount      float64 `json:"amount"`
    Description string  `json:"description"`
    Date        string  `json:"date"`
}

func (h *TransactionHandler) CreateTransaction(w http.ResponseWriter, r *http.Request) {
    defer r.Body.Close()

    var req CreateTransactionRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid request body", http.StatusBadRequest)
        return
    }

    date, err := time.Parse("2006-01-02", req.Date)
    if err != nil {
        http.Error(w, "invalid date format, use YYYY-MM-DD", http.StatusBadRequest)
        return
    }

    userID := 1 // временно

    transaction, err := h.transactionService.CreateTransaction(
        r.Context(),
        userID,
        req.CategoryID,
        req.Amount,
        req.Description,
        date,
    )
    if err != nil {
        if errors.Is(err, domain.ErrInvalidInput) || errors.Is(err, domain.ErrCategoryDoesNotBelongToUser) {
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }
        if errors.Is(err, domain.ErrCategoryNotFound) {
            http.Error(w, err.Error(), http.StatusNotFound)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(TransactionResponse{
        ID:          transaction.ID,
        UserID:      transaction.UserID,
        CategoryID:  transaction.CategoryID,
        Amount:      transaction.Amount,
        Description: transaction.Description,
        Date:        transaction.Date.Format("2006-01-02"),
    })
}

func (h *TransactionHandler) GetUserTransactions(w http.ResponseWriter, r *http.Request) {
    userID := 1 // временно

    transactions, err := h.transactionService.GetUserTransactions(r.Context(), userID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    response := make([]TransactionResponse, len(transactions))
    for i, t := range transactions {
        response[i] = TransactionResponse{
            ID:          t.ID,
            UserID:      t.UserID,
            CategoryID:  t.CategoryID,
            Amount:      t.Amount,
            Description: t.Description,
            Date:        t.Date.Format("2006-01-02"),
        }
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}