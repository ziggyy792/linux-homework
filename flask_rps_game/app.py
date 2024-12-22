from flask import Flask, request, render_template
import sqlite3
from random import choice

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    player_choice = request.form['choice']
    computer_choice = choice(['Rock', 'Paper', 'Scissors'])
    result = determine_winner(player_choice, computer_choice)
    conn = get_db_connection()
    conn.execute('INSERT INTO game_results (player_choice, computer_choice, result) VALUES (?, ?, ?)',
                 (player_choice, computer_choice, result))
    conn.commit()
    conn.close()
    return render_template('index.html', computer_choice=computer_choice, result=result)

def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == 'Rock' and computer == 'Scissors') or \
         (player == 'Scissors' and computer == 'Paper') or \
         (player == 'Paper' and computer == 'Rock'):
        return "You win!"
    elif (player == 'Rock' and computer == 'Paper') or \
         (player == 'Scissors' and computer == 'Rock') or \
         (player == 'Paper' and computer == 'Scissors'):
        return "You lose!"
    else:
        return "Error: Invalid choices"
if __name__ == '__main__':
    app.run(debug=True)
