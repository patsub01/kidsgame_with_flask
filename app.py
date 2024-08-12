from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Initialize the target number and the maximum number of attempts
target_number = random.randint(1, 10)
max_attempts = 5

def get_db_connection():
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    global target_number, max_attempts
    attempts_left = max_attempts
    message = ""
    
    if request.method == 'POST':
        guess = int(request.form.get('guess'))
        attempts_left = int(request.form.get('attempts_left')) - 1
        
        if guess < target_number:
            message = "Too low! Try again."
        elif guess > target_number:
            message = "Too high! Try again."
        else:
            message = f"Congratulations! You've guessed the number {target_number}."
            return redirect(url_for('result', message=message, attempts_left=attempts_left))
        
        if attempts_left == 0:
            message = f"Game over! The correct number was {target_number}."
            return redirect(url_for('result', message=message, attempts_left=0))
    
    return render_template('index.html', message=message, attempts_left=attempts_left)

@app.route('/result', methods=['GET', 'POST'])
def result():
    message = request.args.get('message')
    attempts_left = request.args.get('attempts_left')
    
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        score = int(attempts_left)
        
        conn = get_db_connection()
        conn.execute('INSERT INTO scores (player_name, score) VALUES (?, ?)', (player_name, score))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('result.html', message=message)

@app.route('/highscores')
def highscores():
    conn = get_db_connection()
    scores = conn.execute('SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('highscores.html', scores=scores)

if __name__ == "__main__":
    app.run(debug=True)
