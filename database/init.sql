# Database initialization script for the gym-app
# if not already exists, creates the 'users' table with the following columns:
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
#ensure no zero or negative value
    weight_kg DECIMAL(5,2) NOT NULL CHECK (weight_kg > 0),
#automatically set the creatin time
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);