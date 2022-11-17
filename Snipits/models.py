from . import db
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy.sql import func


class Trip(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(10000))
    trip_type = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    num_people = db.Column(db.Integer)
    #how to associate different imformation with different users
    #do this in the form of a foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Friends(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    #1 for waiting on friend1, 2 for waiting on friend2, 0 for active
    status = db.Column(db.Integer)
    # holds the id of the partners friend id
    partner_link = db.Column(db.Integer)
    friend1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend2_id = db.Column(db.Integer)

