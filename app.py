import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ---------- DB CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- HOME / LIST APPLICANTS ----------
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT applicants.id, applicants.name, applicants.email,
               applicants.status, programs.name AS program_name
        FROM applicants
        LEFT JOIN programs ON applicants.program_id = programs.id
    """)
    applicants = cursor.fetchall()
    conn.close()

    return render_template("index.html", applicants=applicants)


# ---------- ADD APPLICANT ----------
@app.route("/add_applicant", methods=["GET", "POST"])
def add_applicant():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        program_id = request.form["program_id"]
        status = request.form["status"]

        cursor.execute(
            "INSERT INTO applicants (name, email, program_id, status) VALUES (?, ?, ?, ?)",
            (name, email, program_id, status)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()
    conn.close()

    return render_template("add_applicant.html", programs=programs)


# ---------- EDIT PROGRAM ----------
@app.route("/edit_applicant/<int:id>", methods=["GET", "POST"])
def edit_applicant(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        program_id = request.form["program_id"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE applicants
            SET name=?, email=?, program_id=?, status=?
            WHERE id=?
        """, (name, email, program_id, status, id))

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM applicants WHERE id=?", (id,))
    applicant = cursor.fetchone()

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    conn.close()

    return render_template(
        "edit_program.html",
        applicant=applicant,
        programs=programs
    )

@app.route("/delete_applicant/<int:id>")
def delete_applicant(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM applicants WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)