from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    date_creation = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return ("<User %r>" % self.id )

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST" :
        user = User(
            username = request.form["username"],
            email = request.form["email"],
        )
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        except :
            return 'There was an unknown issue adding a user'
    else:
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        return render_template('index.html', users = users)

@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.commit()
        return redirect("/")
    except:
        return 'There was an issue deleting the user'

with app.app_context():
    db.create_all()
app.run(debug=True)