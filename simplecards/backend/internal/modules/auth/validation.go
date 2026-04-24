package auth

import (
	"errors"
	"net/mail"
	"strings"
)

func normalizeLoginRequest(req loginRequest) loginRequest {
	req.Email = strings.TrimSpace(strings.ToLower(req.Email))
	req.Password = strings.TrimSpace(req.Password)

	return req
}

func validateLoginRequest(req loginRequest) error {
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
