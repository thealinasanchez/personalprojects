```mermaid
erDiagram
    USERS {
        uuid id PK
        varchar email UK
        varchar username UK
        text password_hash
        timestamptz created_at
        timestamptz updated_at
    }

    FOLDERS {
        uuid id PK
        uuid owner_user_id FK
        varchar name
        text description
        timestamptz created_at
        timestamptz updated_at
    }

    STUDY_SETS {
        uuid id PK
        uuid owner_user_id FK
        varchar title
        text description
        varchar visibility
        timestamptz created_at
        timestamptz updated_at
    }

    FOLDER_STUDY_SETS {
        uuid folder_id PK
        uuid study_set_id PK
        integer position
        timestamptz added_at
    }

    FLASHCARDS {
        uuid id PK
        uuid study_set_id FK
        text term
        text definition
        integer position
        timestamptz created_at
        timestamptz updated_at
    }

    USER_SECTION_SESSIONS {
        uuid id PK
        uuid user_id FK
        varchar section_name
        timestamptz started_at
        timestamptz ended_at
        integer duration_seconds
    }

    USER_FLASHCARD_PROGRESS {
        uuid id PK
        uuid user_id FK
        uuid flashcard_id FK
        varchar status
        integer times_seen
        integer times_correct
        integer times_incorrect
        boolean is_favorited
        timestamptz favorited_at
        timestamptz last_studied_at
        timestamptz last_reviewed_at
        timestamptz next_review_at
        integer consecutive_correct_count
        timestamptz mastered_at
        timestamptz created_at
        timestamptz updated_at
    }

    STUDY_SESSIONS {
        uuid id PK
        uuid user_id FK
        uuid study_set_id FK
        varchar session_type
        varchar study_mode
        timestamptz started_at
        timestamptz ended_at
        integer duration_seconds
        integer planned_focus_seconds
        integer planned_break_seconds
        integer completed_cycles
        integer cards_reviewed_count
        integer cards_correct_count
        integer cards_incorrect_count
        timestamptz created_at
    }

    USER_STATS {
        uuid user_id PK
        integer total_points
        integer current_streak_days
        integer longest_streak_days
        integer total_cards_studied
        integer total_sets_studied
        date last_study_date
        timestamptz updated_at
    }

    BADGES {
        uuid id PK
        varchar code UK
        varchar name
        text description
        integer points_reward
        timestamptz created_at
    }

    USER_BADGES {
        uuid id PK
        uuid user_id FK
        uuid badge_id FK
        timestamptz awarded_at
    }

    STUDY_GROUPS {
        uuid id PK
        uuid owner_user_id FK
        varchar name
        text description
        varchar visibility
        timestamptz created_at
        timestamptz updated_at
    }

    STUDY_GROUP_MEMBERS {
        uuid group_id PK
        uuid user_id PK
        varchar role
        timestamptz joined_at
    }

    GROUP_MESSAGES {
        uuid id PK
        uuid group_id FK
        uuid sender_user_id FK
        uuid parent_message_id FK
        text message_body
        varchar message_type
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    GROUP_CHECK_INS {
        uuid id PK
        uuid group_id FK
        uuid created_by_user_id FK
        uuid source_message_id FK
        uuid result_message_id FK
        varchar check_in_type
        varchar response_format
        text prompt_text
        timestamptz starts_at
        timestamptz expires_at
        boolean locks_when_all_responded
        boolean is_locked
        timestamptz created_at
    }

    GROUP_CHECK_IN_RESPONSES {
        uuid id PK
        uuid check_in_id FK
        uuid user_id FK
        boolean boolean_response
        text text_response
        timestamptz responded_at
    }

    GROUP_STUDY_SETS {
        uuid group_id PK
        uuid study_set_id PK
        uuid added_by_user_id FK
        timestamptz added_at
    }

    USER_DASHBOARD_PREFERENCES {
        uuid user_id PK
        boolean show_streaks
        boolean show_due_reviews
        boolean show_favorites
        boolean show_recent_sessions
        boolean show_group_activity
        boolean show_points
        boolean show_badges
        boolean show_study_time
        timestamptz updated_at
    }

    USERS ||--o{ FOLDERS : owns
    USERS ||--o{ STUDY_SETS : owns
    FOLDERS ||--o{ FOLDER_STUDY_SETS : contains
    STUDY_SETS ||--o{ FOLDER_STUDY_SETS : assigned_to
    STUDY_SETS ||--o{ FLASHCARDS : has

    USERS ||--o{ USER_SECTION_SESSIONS : logs
    USERS ||--o{ USER_FLASHCARD_PROGRESS : tracks
    FLASHCARDS ||--o{ USER_FLASHCARD_PROGRESS : has_progress

    USERS ||--o{ STUDY_SESSIONS : performs
    STUDY_SETS ||--o{ STUDY_SESSIONS : used_in

    USERS ||--|| USER_STATS : has
    USERS ||--o{ USER_BADGES : earns
    BADGES ||--o{ USER_BADGES : awarded_as

    USERS ||--o{ STUDY_GROUPS : owns
    STUDY_GROUPS ||--o{ STUDY_GROUP_MEMBERS : has
    USERS ||--o{ STUDY_GROUP_MEMBERS : joins

    STUDY_GROUPS ||--o{ GROUP_MESSAGES : contains
    USERS ||--o{ GROUP_MESSAGES : sends
    GROUP_MESSAGES ||--o{ GROUP_MESSAGES : parent

    STUDY_GROUPS ||--o{ GROUP_CHECK_INS : has
    USERS ||--o{ GROUP_CHECK_INS : creates
    GROUP_MESSAGES ||--|| GROUP_CHECK_INS : source_message
    GROUP_MESSAGES o|--|| GROUP_CHECK_INS : result_message

    GROUP_CHECK_INS ||--o{ GROUP_CHECK_IN_RESPONSES : receives
    USERS ||--o{ GROUP_CHECK_IN_RESPONSES : submits

    STUDY_GROUPS ||--o{ GROUP_STUDY_SETS : links
    STUDY_SETS ||--o{ GROUP_STUDY_SETS : shared_in
    USERS ||--o{ GROUP_STUDY_SETS : added_by

    USERS ||--|| USER_DASHBOARD_PREFERENCES : customizes
```