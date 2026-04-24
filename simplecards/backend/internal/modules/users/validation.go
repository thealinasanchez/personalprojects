package users

import (
	"errors"
	"strings"

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
	req.Email = strings.TrimSpace(req.Email)
	req.Username = strings.TrimSpace(req.Username)
	req.PasswordHash = strings.TrimSpace(req.PasswordHash)

	return req
}

func validateCreateUserRequest(req createUserRequest) error {
	if req.Email == "" {
		return errors.New("email is required")
	}

	if req.Username == "" {
		return errors.New("username is required")
	}

	if req.PasswordHash == "" {
		return errors.New("password_hash is required")
	}

	return nil
}
