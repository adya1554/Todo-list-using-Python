from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

def get_connection():
    return pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost\SQLEXPRESS;'
        r'DATABASE=TodoDB;'
        r'Trusted_Connection=yes;'
    )


# Get all todos
def get_todos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, checked FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return todos

# Add a new todo
def add_todo(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Delete a todo
def delete_todo(todo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form.get("todo_name")
        if todo_name.strip():  # ✅ Now this only runs when POST
            add_todo(todo_name)
        return redirect(url_for("home"))  # ✅ return after POST

    todos = get_todos()  # ✅ only runs during GET
    return render_template("index.html", items=todos)
 


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    delete_todo(todo_id)
    return redirect(url_for("home"))  

if __name__ == "__main__":
    app.run(debug=True)
