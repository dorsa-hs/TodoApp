from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    is_completed = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list = Todo.query.all() 
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route('/about')
def about():
    return "about page"

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, is_completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_item_id>')
def update(todo_item_id):
    todo_item = Todo.query.filter_by(id=todo_item_id).first()
    todo_item.is_completed = not todo_item.is_completed
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
