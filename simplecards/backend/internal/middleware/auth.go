package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/golang-jwt/jwt/v5"
)

type contextKey string

const (
	userIDKey   contextKey = "user_id"
	emailKey    contextKey = "email"
	usernameKey contextKey = "username"
)

type AuthMiddleware struct {
	jwtSecret string
}

func NewAuthMiddleware(jwtSecret string) *AuthMiddleware {
	return &AuthMiddleware{
		jwtSecret: jwtSecret,
	}
}

func (m *AuthMiddleware) RequireAuth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")

		if authHeader == "" {
			writeError(w, http.StatusUnauthorized, "authorization header is required")
			return
		}

		if !strings.HasPrefix(authHeader, "Bearer ") {
			writeError(w, http.StatusUnauthorized, "authorization header must use Bearer token")
			return
		}

		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		tokenString = strings.TrimSpace(tokenString)

		if tokenString == "" {
			writeError(w, http.StatusUnauthorized, "token is required")
			return
		}

		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (any, error) {
			return []byte(m.jwtSecret), nil
		})

		if err != nil || !token.Valid {
			writeError(w, http.StatusUnauthorized, "invalid or expired token")
			return
		}

		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			writeError(w, http.StatusUnauthorized, "invalid token claims")
			return
		}

		userID, ok := claims["user_id"].(string)
		if !ok || userID == "" {
			writeError(w, http.StatusUnauthorized, "invalid token user id")
			return
		}

		email, _ := claims["email"].(string)
		username, _ := claims["username"].(string)

		ctx := context.WithValue(r.Context(), userIDKey, userID)
		ctx = context.WithValue(ctx, emailKey, email)
		ctx = context.WithValue(ctx, usernameKey, username)

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

func UserIDFromContext(ctx context.Context) string {
	userID, _ := ctx.Value(userIDKey).(string)
	return userID
}

func EmailFromContext(ctx context.Context) string {
	email, _ := ctx.Value(emailKey).(string)
	return email
}

func UsernameFromContext(ctx context.Context) string {
	username, _ := ctx.Value(usernameKey).(string)
	return username
}
