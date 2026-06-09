from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

def init_db():
    try:
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

        print("Table created successfully")

    except Exception as e:
        print("Database Error:", e)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO feedback
            (name, rno, dept, year, domain, experience, skills, specific)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form.get("name"),
                request.form.get("rno"),
                request.form.get("dept"),
                request.form.get("year"),
                request.form.get("domain"),
                request.form.get("experience"),
                request.form.get("skills"),
                request.form.get("specific")
            ))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect("/view")

        except Exception as e:
            return f"Database Error: {e}"

    return render_template("index.html")

@app.route("/view")
def view():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM feedback
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("view.html", data=data)

    except Exception as e:
        return f"Database Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
