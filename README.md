# 🚀 Daily Quiz Challenge

A full-stack web application designed to encourage consistent learning through gamification and a daily streak mechanism. 

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Werkzeug Security
* **Database:** PostgreSQL, psycopg2
* **Frontend:** HTML5, Bootstrap 5, Vanilla JavaScript (Fetch API)

## ✨ Key Features
* **Secure User Authentication:** Implemented password hashing and secure session management for individualized user profiles.
* **Daily Streak Tracking:** Custom backend logic calculates consecutive days played, rewarding user consistency and resetting upon missed days.
* **Dynamic API Endpoints:** RESTful routes fetch randomized, category-specific question sets from a relational database.
* **Responsive UI:** A clean, mobile-friendly interface built with Bootstrap 5, featuring asynchronous DOM updates without page reloads.

## 🗄️ Database Schema
The PostgreSQL database is normalized to track user progression and quiz data:
* `users`: Stores `id`, `username`, `password_hash`, `streak_count`, and `last_played_date`.
* `questions`: Stores categorization (`topic`), the question string, four multiple-choice options, and the correct validation key.
* `quiz_attempt`: Logs a historical record of all completed quizzes, linking `user_id` to scores and timestamps.

## 🚀 Local Installation
1. Clone the repository: `git clone https://github.com/YourUsername/daily-quiz-app.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Set up the local PostgreSQL database.
5. Run the application: `python main.py`
