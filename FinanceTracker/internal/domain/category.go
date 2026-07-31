package domain

type Category struct {
	ID     int
	UserID int
	Name   string
	Type   string
}

func NewCategory(userID int, name, categoryType string) (*Category, error) {
	if name == "" {
		return nil, ErrInvalidInput
	}
	if !(categoryType == "income" || categoryType == "expense") {
		return nil, ErrInvalidInput
	}
	return &Category{UserID: userID, Name: name, Type: categoryType}, nil
}