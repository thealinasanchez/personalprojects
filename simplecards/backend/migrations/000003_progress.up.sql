CREATE TABLE user_section_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    section_name VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    duration_seconds INTEGER
);

CREATE TABLE user_flashcard_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    flashcard_id UUID NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'new',
    times_seen INTEGER NOT NULL DEFAULT 0,
    times_correct INTEGER NOT NULL DEFAULT 0,
    times_incorrect INTEGER NOT NULL DEFAULT 0,
    is_favorited BOOLEAN NOT NULL DEFAULT FALSE,
    favorited_at TIMESTAMPTZ,
    last_studied_at TIMESTAMPTZ,
    last_reviewed_at TIMESTAMPTZ,
    next_review_at TIMESTAMPTZ,
    consecutive_correct_count INTEGER NOT NULL DEFAULT 0,
    mastered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, flashcard_id)
);

CREATE TABLE study_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    study_set_id UUID NOT NULL REFERENCES study_sets(id) ON DELETE CASCADE,
    session_type VARCHAR(50) NOT NULL,
    study_mode VARCHAR(50) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    planned_focus_seconds INTEGER,
    planned_break_seconds INTEGER,
    completed_cycles INTEGER NOT NULL DEFAULT 0,
    cards_reviewed_count INTEGER NOT NULL DEFAULT 0,
    cards_correct_count INTEGER NOT NULL DEFAULT 0,
    cards_incorrect_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
