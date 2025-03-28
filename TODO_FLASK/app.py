from flask import Flask,g,render_template,request,redirect,url_for,flash
import sqlite3


app = Flask(__name__)
database = 'todo_list.db'
app.secret_key = "hamza" 

def get_db():
    db = getattr(g,"_database",None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        db.execute("CREATE TABLE IF NOT EXISTS list(TASK TEXT NOT NULL UNIQUE)")
        db.commit()
    return db
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('_database',None)
    if db is not None:
        db.close()


@app.route("/",methods=['POST','GET'])
def home():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        todo =  request.form['task']
        action = request.form.get("Add")
        if action == 'Add':
            try:
                cursor.execute("INSERT INTO list(TASK) values(?)",(todo,))
                db.commit()
                flash(f"{todo}, Added successfuly", "success")
            except sqlite3.IntegrityError:
                flash(F"{todo}, already exit in list","danger")
            
    cursor.execute("SELECT TASK FROM list")
    tasks = [row[0] for row in cursor.fetchall()]
    return render_template("main.html", tasks=tasks)


@app.route("/delete/<task>", methods=['POST'])
def delete(task):
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute("delete from list where TASK = ?",(task,))
        db.commit()
        flash(f"{task}, deleted successfuly", "success")
        return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)