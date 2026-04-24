package users

import (
	"errors"
	"net/mail"
	"strings"
	"unicode"

	"github.com/google/uuid"
)

var ErrInvalidUserID = errors.New("invalid user id")

func validateUserID(id string) error {
	if _, err := uuid.Parse(id); err != nil {
		return ErrInvalidUserID
	}

	return nil
}

func normalizeCreateUserRequest(req createUserRequest) createUserRequest {
	req.Email = strings.TrimSpace(strings.ToLower(req.Email))
	req.Username = strings.TrimSpace(req.Username)
	req.Password = strings.TrimSpace(req.Password)

	return req
}

func validateCreateUserRequest(req createUserRequest) error {
	if req.Email == "" {
		return errors.New("email is required")
	}

	if _, err := mail.ParseAddress(req.Email); err != nil {
		return errors.New("email must be valid")
	}

	if req.Username == "" {
		return errors.New("username is required")
	}

	if len(req.Username) < 3 {
		return errors.New("username must be at least 3 characters")
	}

	if len(req.Username) > 50 {
		return errors.New("username must be 50 characters or fewer")
	}

	for _, char := range req.Username {
		if !unicode.IsLetter(char) && !unicode.IsDigit(char) && char != '_' {
			return errors.New("username can only contain letters, numbers, and underscores")
		}
	}

	if req.Password == "" {
		return errors.New("password is required")
	}

	if len(req.Password) < 8 {
		return errors.New("password must be at least 8 characters")
	}

	return nil
}

func normalizeLoginUserRequest(req loginUserRequest) loginUserRequest {
	req.Email = strings.TrimSpace(strings.ToLower(req.Email))
	req.Password = strings.TrimSpace(req.Password)

	return req
}

func validateLoginUserRequest(req loginUserRequest) error {
	if req.Email == "" {
		return errors.New("email is required")
	}

	if _, err := mail.ParseAddress(req.Email); err != nil {
		return errors.New("email must be valid")
	}

	if req.Password == "" {
		return errors.New("password is required")
	}

	return nil
}
