from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "birthday.db"

current_choices = {}


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            secret_answer TEXT,
            place TEXT,
            breakfast TEXT,
            afternoon TEXT,
            cake TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("page1.html")


@app.route("/secret", methods=["GET", "POST"])
def secret():

    if request.method == "POST":

        answer = request.form.get("answer")

        if answer == "Village":

            current_choices["secret_answer"] = "1"

            return redirect("/page2")

        return render_template("secret.html", wrong=True)

    return render_template("secret.html", wrong=False)


@app.route("/page2", methods=["GET", "POST"])
def page2():

    if request.method == "POST":

        current_choices["place"] = request.form.get("place")

        return redirect("/page3")

    return render_template("page2.html")


@app.route("/page3", methods=["GET", "POST"])
def page3():

    if request.method == "POST":

        current_choices["breakfast"] = request.form.get("breakfast")
        current_choices["afternoon"] = request.form.get("afternoon")

        return redirect("/page4")

    return render_template("page3.html")


@app.route("/page4", methods=["GET", "POST"])
def page4():

    if request.method == "POST":

        current_choices["cake"] = request.form.get("cake")

        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO choices
            (secret_answer, place, breakfast, afternoon, cake)
            VALUES (?, ?, ?, ?, ?)
        """, (
            current_choices.get("secret_answer", ""),
            current_choices.get("place", ""),
            current_choices.get("breakfast", ""),
            current_choices.get("afternoon", ""),
            current_choices.get("cake", "")
        ))

        conn.commit()
        conn.close()

        return redirect("/final")

    return render_template("page4.html")


@app.route("/final")
def final():
    return render_template("final.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    data = conn.execute("""
        SELECT *
        FROM choices
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template("admin.html", choices=data)


init_db()


if __name__ == "__main__":
    app.run(debug=True)