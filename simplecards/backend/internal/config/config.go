package config

import (
	"fmt"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

type Config struct {
	DBHost        string
	DBPort        string
	DBUser        string
	DBPassword    string
	DBName        string
	DBSSLMode     string
	JWTSecret     string
	AllowedOrigin string
	ServerPort    string
}

func Load() (Config, error) {
	_ = godotenv.Load()

	cfg := Config{
		DBHost:        os.Getenv("DB_HOST"),
		DBPort:        os.Getenv("DB_PORT"),
		DBUser:        os.Getenv("DB_USER"),
		DBPassword:    os.Getenv("DB_PASSWORD"),
		DBName:        os.Getenv("DB_NAME"),
		DBSSLMode:     os.Getenv("DB_SSLMODE"),
		JWTSecret:     os.Getenv("JWT_SECRET"),
		AllowedOrigin: os.Getenv("ALLOWED_ORIGIN"),
		ServerPort:    os.Getenv("SERVER_PORT"),
	}

	if err := cfg.Validate(); err != nil {
		return Config{}, err
	}

	return cfg, nil
}

func (c Config) Validate() error {
	if c.DBHost == "" {
		return fmt.Errorf("DB_HOST is required")
	}
	if c.DBPort == "" {
		return fmt.Errorf("DB_PORT is required")
	}
	if c.DBUser == "" {
		return fmt.Errorf("DB_USER is required")
	}
	if c.DBPassword == "" {
		return fmt.Errorf("DB_PASSWORD is required")
	}
	if c.DBName == "" {
		return fmt.Errorf("DB_NAME is required")
	}
	if c.DBSSLMode == "" {
		return fmt.Errorf("DB_SSLMODE is required")
	}
	if c.JWTSecret == "" {
		return fmt.Errorf("JWT_SECRET is required")
	}
	if c.AllowedOrigin == "" {
		return fmt.Errorf("ALLOWED_ORIGIN is required")
	}
	if c.ServerPort == "" {
		return fmt.Errorf("SERVER_PORT is required")
	}

	// Validate DB port
	dbPort, err := strconv.Atoi(c.DBPort)
	if err != nil {
		return fmt.Errorf("DB_PORT must be a number")
	}
	if dbPort < 1 || dbPort > 65535 {
		return fmt.Errorf("DB_PORT must be between 1 and 65535")
	}

	// Validate server port
	serverPort, err := strconv.Atoi(c.ServerPort)
	if err != nil {
		return fmt.Errorf("SERVER_PORT must be a number")
	}
	if serverPort < 1 || serverPort > 65535 {
		return fmt.Errorf("SERVER_PORT must be between 1 and 65535")
	}

	return nil
}

func (c Config) ServerAddr() string {
	return ":" + c.ServerPort
}

func (c Config) DBConnString() string {
	return fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		c.DBHost,
		c.DBPort,
		c.DBUser,
		c.DBPassword,
		c.DBName,
		c.DBSSLMode,
	)
}
