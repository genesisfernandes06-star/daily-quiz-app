from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from datetime import date, timedelta

app = Flask(__name__)
# This secret key allows Flask to securely remember who is logged in
app.secret_key = "super_secret_bca_key_change_me_later" 

# Standard DB Config for your local setup
DB_CONFIG = {
    "dbname": "quiz_db",
    "user": "postgres",
    "password": "1111",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

# --- User Registration Route ---
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Encrypt the password before saving it to the database
    hashed_pw = generate_password_hash(password)

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
            (username, hashed_pw)
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Registration successful! You can now log in."}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    except Exception as e:
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# --- User Login Route ---
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        # Check if user exists and if the hashed password matches the input
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0] 
            session['username'] = username
            return jsonify({"message": f"Welcome back, {username}!"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# --- Fetch Quiz Questions Route ---
@app.route("/api/quiz", methods=["GET"])
def get_quiz():
    chosen_topic = request.args.get('topic')
    
    if not chosen_topic:
        return jsonify({"error": "Please select a category first"}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option 
            FROM questions 
            WHERE topic = %s 
            ORDER BY RANDOM() 
            LIMIT 5
        """
        cur.execute(query, (chosen_topic,))
        rows = cur.fetchall()
        
        if not rows:
            return jsonify({"message": f"No questions found for {chosen_topic}"}), 404

        questions = [{
            "id": r[0], 
            "question": r[1], 
            "options": {"A": r[2], "B": r[3], "C": r[4], "D": r[5]},
            "correct": r[6]
        } for r in rows]
        
        cur.close()
        return jsonify(questions)
        
    except Exception as e:
        print("CRITICAL DATABASE ERROR:", e)
        return jsonify({"error": "Database connection failed"}), 500
    finally:
        if conn:
            conn.close()

# --- Submit Score & Calculate Daily Streak ---
@app.route("/api/submit", methods=["POST"])
def submit_score():
    if 'user_id' not in session:
        return jsonify({"error": "Please log in to track your streak!"}), 401
        
    user_id = session['user_id']
    data = request.json
    score = data.get("score", 0)
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get the user's current streak and the last date they played
        cur.execute("SELECT streak_count, last_played_date FROM users WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        
        current_streak = user_data[0] if user_data[0] else 0
        last_played = user_data[1]
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Streak Calculation
        new_streak = current_streak
        if last_played == today:
            pass # Already played today, streak stays the same
        elif last_played == yesterday:
            new_streak += 1 # Consecutive day, increase streak
        else:
            new_streak = 1 # Missed a day, streak resets to 1
            
        # Update the users table
        cur.execute(
            "UPDATE users SET streak_count = %s, last_played_date = %s WHERE id = %s", 
            (new_streak, today, user_id)
        )
        
        # Log this quiz attempt
        cur.execute(
            "INSERT INTO quiz_attempt (user_id, score, attempt_date) VALUES (%s, %s, %s)",
            (user_id, score, today)
        )
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "message": "Score saved successfully!", 
            "score": score, 
            "streak": new_streak
        }), 200
        
    except Exception as e:
        print("Streak calculation error:", e)
        return jsonify({"error": "Failed to save score"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)