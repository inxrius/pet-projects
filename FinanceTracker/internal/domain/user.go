package domain

import "strings"

type User struct {
	ID    int
	Name  string
	Email string
}

func NewUser(name, email string) (*User, error) {
	if name == "" {
		return nil, ErrInvalidInput
	}
	if !strings.Contains(email, "@") {
		return nil, ErrInvalidInput
	}
	return &User{Name: name, Email: strings.ToLower(email)}, nil
}
