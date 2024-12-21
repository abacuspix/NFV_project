from dbhelper import DBHelper
from flask import Flask, render_template, request

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    """
    Displays the home page with all the data fetched from the database.
    """
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(f"Error fetching data: {e}")
        data = None
    return render_template("home.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    """
    Adds user input to the database.
    """
    try:
        data = request.form.get("userinput")
        if data:  # Ensure user input is not empty
            DB.add_input(data)
    except Exception as e:
        print(f"Error adding input: {e}")
    return home()


@app.route("/clear")
def clear():
    """
    Clears all data from the database.
    """
    try:
        DB.clear_all()
    except Exception as e:
        print(f"Error clearing data: {e}")
    return home()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
