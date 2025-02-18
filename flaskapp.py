from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

DATABASE = "users.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        
        # File Upload Handling
        file = request.files['file']
        word_count = 0
        file_path = None

        if file:
            content = file.read().decode('utf-8')
            word_count = len(content.split())
            file_path = os.path.join(UPLOAD_FOLDER, f"{username}_uploaded.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, firstname, lastname, email, word_count) VALUES (?, ?, ?, ?, ?, ?)", 
                       (username, password, firstname, lastname, email, word_count))
        conn.commit()
        conn.close()
        
        return redirect(url_for('profile', username=username))
    
    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template('profile.html', user=user)
    return "User not found", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('profile', username=username))
        else:
            return "Invalid credentials. Try again."
    
    return render_template('login.html')

@app.route('/download/<username>')
def download(username):
    file_path = os.path.join(UPLOAD_FOLDER, f"{username}_uploaded.txt")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
