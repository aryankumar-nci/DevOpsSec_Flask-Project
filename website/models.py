from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email =db.Column(db.String(150), unique=True)
    username=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    #fill with current time
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    

#workouts
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(150), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)