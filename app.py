
import json
import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager,UserMixin
from flask_restful import Api,Resource
from werkzeug.utils import secure_filename
import os



app=Flask(__name__)
app.config['SECRET_KEY']='8efde650d0e727ef697bb75adb2a114a'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userData.db'
app.config['SQLALCHEMY_BINDS']={
    'posts':'sqlite:///posts.db',
    'comment':'sqlite:///comment.db',
    'vote':'sqlite:///vote.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False 

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#database model
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(60),nullable=False)
    colleague=db.Column(db.String(500),default=",")
    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"


class Posts(db.Model):
    __bind_key__='posts'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer)
    caption=db.Column(db.String(200))
    username=db.Column(db.String(40))

class Comment(db.Model):
    __bind_key__='comment'
    id=db.Column(db.Integer,primary_key=True)
    com=db.Column(db.String(150))
    uid=db.Column(db.Integer)
    pid=db.Column(db.Integer)


from routes import *

if __name__=="__main__":
    app.run(debug=True)