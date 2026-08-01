package handler

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"

	"github.com/inxrius/FinanceTracker/internal/service"
)

type CreateUserRequest struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

type UserHandler struct {
	userService *service.UserService
}

func NewUserHandler(userService *service.UserService) *UserHandler {
	return &UserHandler{userService}
}

func (h UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	contentType := r.Header.Get("Content-Type")
	if contentType != "application/json" {
		http.Error(w, "Content-Type must be application/json", http.StatusUnsupportedMediaType)
		return
	}

	// Создаём переменную для данных
	var user CreateUserRequest

	// Создаём декодер и включаем строгий режим
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields() // Ошибка, если в JSON есть лишние поля

	// Декодируем JSON в структуру
	err := decoder.Decode(&user)
	if err != nil {
		// Детальная обработка ошибок
		var syntaxError *json.SyntaxError
		if errors.As(err, &syntaxError) {
			http.Error(w, fmt.Sprintf("Invalid JSON: %s (at position %d)", err.Error(), syntaxError.Offset), http.StatusBadRequest)
		} else {
			http.Error(w, err.Error(), http.StatusBadRequest)
		}
		return
	}

	// Дополнительная валидация полей
	if user.Name == "" {
		http.Error(w, "Name is required", http.StatusBadRequest)
		return
	}
	if user.Email == "" {
		http.Error(w, "Email is required", http.StatusBadRequest)
		return
	}

	// Здесь можно хешировать пароль или сохранять пользователя в базу

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}
