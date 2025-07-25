from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))
    ConfirmPassword = db.Column(db.String(100))

with app.app_context():
    #db.drop_all()
    db.create_all()