from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    task_list = Todo.query.all()

    return render_template('base.html', task_list=task_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Todo(title=title, complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:task_id>")
def update(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/listalltasks")
def lists():
    lists = Todo.query.all()
    return render_template("lists.html", lists=lists)


if __name__ == "__main__":
    app.run(debug=True)
