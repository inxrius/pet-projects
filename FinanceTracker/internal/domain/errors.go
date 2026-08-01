package domain

import "errors"

var (
	ErrUserNotFound            = errors.New("user not found")
	ErrCategoryNotFound        = errors.New("category not found")
	ErrTransactionNotFound     = errors.New("transaction not found")
	ErrInvalidInput            = errors.New("invalid input")
	ErrCategoryHasTransactions = errors.New("can't delete category with transactions")
)