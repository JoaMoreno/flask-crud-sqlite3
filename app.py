from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/tasks.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreCurso = db.Column(db.String(200))
    descripcion = db.Column(db.String(200))
    porcentaje = db.Column(db.Integer())
    done = db.Column(db.Boolean)


@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template("base.html", tasks = tasks)

@app.route("/create-task", methods=["POST"])
def create():
    task = Task(nombreCurso=request.form["nombreCurso"], done=False,porcentaje=request.form["porcentaje"],descripcion=request.form["descripcion"])
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("cursos"))

#========== CURSOS ==========#
@app.route("/cursos")
def cursos():
    tasks = Task.query.all()
    return render_template("cursos.html", tasks = tasks)

@app.route("/cursos/add")
def addCurso():
    return render_template("addCurso.html")

#========== BTN CURSOS ==========#
@app.route("/addp/<id>")
def addp(id):
    task = Task.query.filter_by(id=int(id)).first()
    if task.porcentaje >= 0 and task.porcentaje < 100:
        task.porcentaje = task.porcentaje + 5
    db.session.commit()
    return redirect(url_for("cursos"))

@app.route("/sustp/<id>")
def sustp(id):
    task = Task.query.filter_by(id=int(id)).first()
    if task.porcentaje > 0 and task.porcentaje <= 100:
        task.porcentaje = task.porcentaje - 5
    db.session.commit()
    return redirect(url_for("cursos"))

@app.route("/done/<id>")
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for("cursos"))

@app.route("/delete/<id>")
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("cursos"))

if __name__ == "__main__":
    app.run(debug=True)