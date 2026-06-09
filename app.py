from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# HOME PAGE (FORM)
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        name = request.form["name"]
        rno = request.form["rno"]
        dept = request.form["dept"]
        year = request.form["year"]
        domain = request.form["domain"]
        experience = request.form["experience"]
        skills = request.form["skills"]
        specific = request.form["specific"]

        conn = sqlite3.connect("feedback.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO feedback
        (name,rno,dept,year,domain,experience,skills,specific)
        VALUES (?,?,?,?,?,?,?,?)
        """,
        (name,rno,dept,year,domain,experience,skills,specific))

        conn.commit()
        conn.close()

        return "Feedback Saved Successfully!"

    return render_template("index.html")


# VIEW PAGE
@app.route("/view")
def view():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    data = cursor.fetchall()
    conn.close()
    return render_template("view.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
