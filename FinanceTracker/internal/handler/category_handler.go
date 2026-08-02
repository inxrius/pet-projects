package handler

import (
    "encoding/json"
    "errors"
    "net/http"
    "strconv"

    "github.com/go-chi/chi/v5"
    "github.com/inxrius/FinanceTracker/internal/domain"
    "github.com/inxrius/FinanceTracker/internal/service"
)

type CategoryHandler struct {
    categoryService *service.CategoryService
}

func NewCategoryHandler(categoryService *service.CategoryService) *CategoryHandler {
    return &CategoryHandler{categoryService: categoryService}
}

type CreateCategoryRequest struct {
    Name string `json:"name"`
    Type string `json:"type"`
}

type CategoryResponse struct {
    ID     int    `json:"id"`
    UserID int    `json:"user_id"`
    Name   string `json:"name"`
    Type   string `json:"type"`
}

func (h *CategoryHandler) CreateCategory(w http.ResponseWriter, r *http.Request) {
    defer r.Body.Close()

    var req CreateCategoryRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid request body", http.StatusBadRequest)
        return
    }

    // Пока нет аутентификации, передаём userID=1 для примера
    userID := 1

    category, err := h.categoryService.CreateCategory(r.Context(), userID, req.Name, req.Type)
    if err != nil {
        if errors.Is(err, domain.ErrInvalidInput) {
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(CategoryResponse{
        ID:     category.ID,
        UserID: category.UserID,
        Name:   category.Name,
        Type:   category.Type,
    })
}

func (h *CategoryHandler) GetUserCategories(w http.ResponseWriter, r *http.Request) {
    userID := 1 // временно

    categories, err := h.categoryService.GetUserCategories(r.Context(), userID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    response := make([]CategoryResponse, len(categories))
    for i, c := range categories {
        response[i] = CategoryResponse{
            ID:     c.ID,
            UserID: c.UserID,
            Name:   c.Name,
            Type:   c.Type,
        }
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (h *CategoryHandler) DeleteCategory(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.Atoi(idStr)
    if err != nil {
        http.Error(w, "invalid category ID", http.StatusBadRequest)
        return
    }

    err = h.categoryService.DeleteCategory(r.Context(), id)
    if err != nil {
        if errors.Is(err, domain.ErrCategoryNotFound) {
            http.Error(w, err.Error(), http.StatusNotFound)
            return
        }
        if errors.Is(err, domain.ErrCategoryHasTransactions) {
            http.Error(w, err.Error(), http.StatusConflict)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusNoContent)
}