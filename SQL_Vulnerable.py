from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        username = request.form.get("username")
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Vulnerable SQL query (string concatenation)
        query = f"SELECT * FROM users WHERE username = '{username}'"
        print(query)
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()
        
        result = "<br>".join([f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}" for user in users])
        if not result:
            result = "No results found."
    
    return render_template_string('''
        <form method="post">
            <label>Search Username:</label>
            <input type="text" name="username" required>
            <button type="submit">Search</button>
        </form>
        <p>{{ result|safe }}</p>
    ''', result=result)

if __name__ == "__main__":
    app.run(debug=True)
