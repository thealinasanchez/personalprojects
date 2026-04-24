package users

type userResponse struct {
	ID        string `json:"id"`
	Email     string `json:"email"`
	Username  string `json:"username"`
	CreatedAt string `json:"created_at"`
}

type createUserRequest struct {
	Email    string `json:"email"`
	Username string `json:"username"`
	Password string `json:"password"`
}

type createUserParams struct {
	Email        string
	Username     string
	PasswordHash string
}
