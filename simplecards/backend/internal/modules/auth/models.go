package auth

type loginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type userResponse struct {
	ID        string `json:"id"`
	Email     string `json:"email"`
	Username  string `json:"username"`
	CreatedAt string `json:"created_at"`
}

type loginResponse struct {
	User  userResponse `json:"user"`
	Token string       `json:"token"`
}

type userWithPasswordHash struct {
	ID           string
	Email        string
	Username     string
	PasswordHash string
	CreatedAt    string
}
