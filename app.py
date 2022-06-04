
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
api=Api(app)
app.config['SECRET_KEY']='8efde650d0e727ef697bb75adb2a114a'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userData.db'
app.config['SQLALCHEMY_BINDS']={
    'posts':'sqlite:///posts.db'
}
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False 

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#centralized

class centralized(Resource):
      def get(self,emailid,password):
        user=User.query.filter_by(email=emailid).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return json.dumps({"rollNo":user.id,"userName":user.username,"email":user.email,"status":True})
        return json.dumps({"status":False})

api.add_resource(centralized,"/centralized/<string:emailid>/<string:password>")



#database model
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(60),nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"


class Posts(db.Model):
    __bind_key__='posts'
    id=db.Column(db.Integer,primary_key=True)
    roll_no=db.Column(db.Integer)
    caption=db.Column(db.String(200))
    username=db.Column(db.String(40))
    appr=db.Column(db.Integer,default=0)
    pic=db.Column(db.String(150))


from routes import *

if __name__=="__main__":
    app.run(debug=True)