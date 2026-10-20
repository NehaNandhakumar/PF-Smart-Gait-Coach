-- 1. Create a table to track different profiles/users
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create a table to log every recorded step
CREATE TABLE IF NOT EXISTS stride_logs (
    stride_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    roll_time_ms INT NOT NULL,               -- The transition time in milliseconds
    gait_classification VARCHAR(50),         -- e.g., 'RAPID_STRIKE', 'PROLONGED_HEEL', 'IDEAL'
    recommended_shoe_type TEXT,              -- The specific recommendation string
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);