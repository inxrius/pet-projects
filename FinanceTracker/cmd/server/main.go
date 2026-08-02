package main

import (
    "log"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
    "github.com/inxrius/FinanceTracker/internal/handler"
    "github.com/inxrius/FinanceTracker/internal/repository/inmemory"
    "github.com/inxrius/FinanceTracker/internal/service"
)

func main() {
    // Инициализация in-memory репозиториев
    userRepo := inmemory.NewUserRepository()
    categoryRepo := inmemory.NewCategoryRepository()
    transactionRepo := inmemory.NewTransactionRepository()

    // Сервисы
    userService := service.NewUserService(userRepo)
    categoryService := service.NewCategoryService(categoryRepo, transactionRepo)
    transactionService := service.NewTransactionService(transactionRepo, categoryRepo)

    // Обработчики
    userHandler := handler.NewUserHandler(userService)
    categoryHandler := handler.NewCategoryHandler(categoryService)
    transactionHandler := handler.NewTransactionHandler(transactionService)

    // Роутер
    r := chi.NewRouter()
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.RequestID)

    r.Route("/api/v1", func(r chi.Router) {
        // Пользователи
        r.Post("/users", userHandler.CreateUser)
        r.Get("/users/{id}", userHandler.GetUser)
        r.Get("/users", userHandler.GetAllUsers)

        // Категории
        r.Post("/categories", categoryHandler.CreateCategory)
        r.Get("/categories", categoryHandler.GetUserCategories)
        r.Delete("/categories/{id}", categoryHandler.DeleteCategory)

        // Транзакции
        r.Post("/transactions", transactionHandler.CreateTransaction)
        r.Get("/transactions", transactionHandler.GetUserTransactions)
    })

    log.Println("Server starting on :8080")
    if err := http.ListenAndServe(":8080", r); err != nil {
        log.Fatal(err)
    }
}