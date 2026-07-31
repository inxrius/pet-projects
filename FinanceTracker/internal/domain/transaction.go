package domain

import "time"

type Transaction struct {
	ID          int
	UserID      int
	CategoryID  int
	Amount      float64
	Description string
	Date        time.Time
}

func NewTransaction(userID, categoryID int, amount float64, description string, date time.Time) (*Transaction, error) {
	if amount <= 0 {
		return nil, ErrInvalidInput
	}
	if description == "" {
		return nil, ErrInvalidInput
	}
	if date.IsZero() {
		return nil, ErrInvalidInput
	}
	return &Transaction{
		UserID: userID,
		CategoryID: categoryID,
		Amount: amount,
		Description: description,
		Date: date,
	}, nil
}