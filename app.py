from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", "5432")
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        name TEXT,
        rno TEXT,
        dept TEXT,
        year TEXT,
        domain TEXT,
        experience TEXT,
        skills TEXT,
        specific TEXT
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO feedback
        (name, rno, dept, year, domain, experience, skills, specific)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form["name"],
            request.form["rno"],
            request.form["dept"],
            request.form["year"],
            request.form["domain"],
            request.form["experience"],
            request.form["skills"],
            request.form["specific"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/view")

    return render_template("index.html")

@app.route("/view")
def view():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, rno, dept, year,
               domain, experience, skills, specific
        FROM feedback
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
