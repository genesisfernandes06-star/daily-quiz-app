-- For pgAdmin later
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE
);
INSERT INTO tasks (title, description) VALUES 
('Daily Quiz Backend Ready', 'Flask PostgreSQL connected for team demo'),
('Quiz Scores API', 'CRUD endpoints working');