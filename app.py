from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      category TEXT NOT NULL,
                      description TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts")
    workouts = cursor.fetchall()
    conn.close()
    return render_template('index.html', workouts=workouts)

@app.route('/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workouts (name, category, description) VALUES (?, ?, ?)",
                       (name, category, description))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_workout.html')

@app.route('/edit/<int:workout_id>', methods=['GET', 'POST'])
def edit_workout(workout_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        
        cursor.execute("UPDATE workouts SET name = ?, category = ?, description = ? WHERE id = ?",
                       (name, category, description, workout_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
    workout = cursor.fetchone()
    conn.close()
    return render_template('edit_workout.html', workout=workout)

@app.route('/delete/<int:workout_id>', methods=['POST'])
def delete_workout(workout_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/view/<int:workout_id>')
def view_workout(workout_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
    workout = cursor.fetchone()
    conn.close()
    return render_template('view_workout.html', workout=workout)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
