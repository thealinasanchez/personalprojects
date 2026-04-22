CREATE TABLE user_dashboard_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    show_streaks BOOLEAN NOT NULL DEFAULT TRUE,
    show_due_reviews BOOLEAN NOT NULL DEFAULT TRUE,
    show_favorites BOOLEAN NOT NULL DEFAULT TRUE,
    show_recent_sessions BOOLEAN NOT NULL DEFAULT TRUE,
    show_group_activity BOOLEAN NOT NULL DEFAULT TRUE,
    show_points BOOLEAN NOT NULL DEFAULT TRUE,
    show_badges BOOLEAN NOT NULL DEFAULT TRUE,
    show_study_time BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
