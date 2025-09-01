from flask import Flask, request, render_template_string
import psycopg2   # for PostgreSQL
import os

app = Flask(__name__)

# AWS RDS credentials via Environment Variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "testdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Simple HTML template
HTML = """
<!DOCTYPE html>
<html>
<head><title>AWS ECS + RDS Demo</title></head>
<body>
  <h1>AWS ECS + RDS (Flask App)</h1>
  <form method="POST">
    <input type="text" name="username" placeholder="Enter Name" required>
    <button type="submit">Submit</button>
  </form>
  <h2>Stored Users:</h2>
  <ul>
    {% for user in users %}
      <li>{{ user }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT)")
    conn.commit()

    if request.method == "POST":
        name = request.form["username"]
        cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()

    cur.execute("SELECT name FROM users")
    rows = cur.fetchall()
    users = [row[0] for row in rows]

    cur.close()
    conn.close()

    return render_template_string(HTML, users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
