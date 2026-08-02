package handler

import (
    "encoding/json"
    "errors"
    "fmt"
    "net/http"
    "strconv"

    "github.com/go-chi/chi/v5"
    "github.com/inxrius/FinanceTracker/internal/domain"
    "github.com/inxrius/FinanceTracker/internal/service"
)

type UserHandler struct {
    userService *service.UserService
}

func NewUserHandler(userService *service.UserService) *UserHandler {
    return &UserHandler{userService: userService}
}

type CreateUserRequest struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}

type UserResponse struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    defer r.Body.Close()

    var req CreateUserRequest
    decoder := json.NewDecoder(r.Body)
    decoder.DisallowUnknownFields()

    if err := decoder.Decode(&req); err != nil {
        var syntaxError *json.SyntaxError
        if errors.As(err, &syntaxError) {
            http.Error(w, fmt.Sprintf("Invalid JSON (at position %d)", syntaxError.Offset), http.StatusBadRequest)
        } else {
            http.Error(w, err.Error(), http.StatusBadRequest)
        }
        return
    }

    user, err := h.userService.Register(r.Context(), req.Name, req.Email)
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
    json.NewEncoder(w).Encode(UserResponse{
        ID:    user.ID,
        Name:  user.Name,
        Email: user.Email,
    })
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.Atoi(idStr)
    if err != nil {
        http.Error(w, "invalid user ID", http.StatusBadRequest)
        return
    }

    user, err := h.userService.GetUser(r.Context(), id)
    if err != nil {
        if errors.Is(err, domain.ErrUserNotFound) {
            http.Error(w, err.Error(), http.StatusNotFound)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(UserResponse{
        ID:    user.ID,
        Name:  user.Name,
        Email: user.Email,
    })
}

func (h *UserHandler) GetAllUsers(w http.ResponseWriter, r *http.Request) {
    users, err := h.userService.GetAllUsers(r.Context())
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    response := make([]UserResponse, len(users))
    for i, u := range users {
        response[i] = UserResponse{
            ID:    u.ID,
            Name:  u.Name,
            Email: u.Email,
        }
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}