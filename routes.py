from re import I
from forms import RegistrationForm,LoginForm
from flask import render_template,flash,redirect,url_for,request
from app import db,bcrypt,app,User,Posts
from flask_login import current_user,login_required,logout_user,login_user
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def hello():
    return render_template('index.html',login=True)


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm(request.form)
    if request.method=='POST' and form.validate():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.userName.data,email=form.emailId.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully ,you may login now!",'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html',login=False,post="Hello "+ current_user.username + ", Welcome to PEER_BLOG")
    form=LoginForm(request.form)
    if request.method=='POST' and form.validate():
        user=User.query.filter_by(email=form.emailId.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            print(current_user.username)
            return render_template('index.html',login=False,post="Hello "+ current_user.username + ", Welcome to INNOVAC'22")
        else:
            flash('Login Unsuccessful. Please check either Email or Password','danger')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))

# @app.route('/media')
# @login_required
# def media():
#     return render_template('home.html',user=current_user.id) 
# @app.route('/feed')
# def feed():
#     P=Posts.query.with_entities(Posts.id).all()
#     P.reverse()
#     p=dict()
#     for i in P:
#         post=Posts.query.filter_by(id=i[0]).first()
#         if(post.appr==1):
#             a=[]
#             a.append(post.caption)
#             a.append(post.username)
#             a.append(post.roll_no)
#             picname='uploads/'+post.pic
#             p[picname]=a
#     print(current_user.id)
#     return render_template('feed.html',dict=p,cid=current_user.id)



# @app.route('/upload')
# def upload():
#     return render_template('upload.html')

# @app.route('/adminfeed')
# @login_required
# def adfeed():
#     P=Posts.query.with_entities(Posts.id).all()
#     P.reverse()
#     print(P)
#     p=dict()
#     for i in P:
#         post=Posts.query.filter_by(id=i[0]).first()
#         print(post.id)
#         a=[]
#         a.append(post.caption)
#         a.append(post.username)
#         a.append(post.roll_no)
#         apr=False
#         if(post.appr==1):
#             apr=True
#         a.append(apr)
#         picname='uploads/'+post.pic
#         p[picname]=a
#     print(p)
#     return render_template('admin.html',dict=p)


# @app.route('/uploader',methods=['GET','POST'])
# @login_required
# def uploader():
#     file = request.files['inputFile']
#     #name tag of form
#     roll_no = current_user.id
#     caption=request.form['caption']
#     username=current_user.username
#     filename=str(roll_no)+'_'+file.filename
#     filename = secure_filename(filename)
  
#     if file and allowed_file(file.filename):
#        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  
#        newFile = Posts(pic=filename, roll_no=roll_no,caption=caption,username=username)
#        db.session.add(newFile)
#        db.session.commit()
#     #    flash('File successfully uploaded ' + file.filename + ' to the database!')
#        return redirect(url_for('feed'))
#     # else:
#     #    flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
#     return redirect(url_for('feed'))
      
# @app.route('/review/<picid>',methods=['GET','POST']) 
# @login_required
# def approve(picid):
#     p=Posts.query.filter_by(pic=picid).first()
#     p.appr=1
#     db.session.commit()
#     return redirect(url_for('adfeed'))

# @app.route('/remove/<picid>',methods=['GET','POST']) 
# @login_required
# def remove(picid):
#     p=Posts.query.filter_by(pic=picid).first()
#     p.appr=0
#     db.session.commit()
#     return redirect(url_for('adfeed'))

@app.route('/feed')
@login_required
def feed():
    P=Posts.query.all()
    d={}
    for i in P:
        G=User.query.filter_by(id=i.uid).first()
        collist=G.colleague
        collist=collist.split(',')
        if(str(current_user.id) in collist):
            ar=[]
            ar.append(i.caption)
            ar.append(i.username)
            d[i.id]=ar
    return render_template('home.html',d=d,user=current_user.username)


@app.route('/colleague')
@login_required
def colleague():
    P=User.query.all()
    dict1={}
    for i in P:
        if(i.id!=current_user.id):
            a=current_user.colleague
            l=a.split(',')
            print(l)
            if(str(i.id) not in l):
                ar=[]
                ar.append(i.username)
                ar.append(i.email)
                dict1[i.id]=ar
    return render_template('colleague.html',d=dict1)

@app.route('/addcol/<identity>',methods=['GET','POST'])
@login_required
def addcol(identity):
    P=User.query.filter_by(id=current_user.id).first()
    print(P.colleague)
    i=P.colleague+str(identity)+','
    print(i)
    P.colleague=i
    db.session.commit()

    return redirect(url_for('colleague'))

@app.route('/uploader',methods=['GET','POST'])
@login_required
def upload():
    uid = current_user.id
    username=current_user.username
    caption=request.form['caption']
    newFile = Posts(uid=uid,caption=caption,username=username)
    db.session.add(newFile)
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    P=Posts.query.all()
    d={}
    for i in P:
        if(i.uid==current_user.id):
            ar=[]
            ar.append(i.caption)
            ar.append(i.username)
            d[i.id]=ar
    return render_template('profile.html',d=d)


@app.route('/delete/<pid>',methods=['GET','POST'])
@login_required
def delete(pid):
    P=Posts.query.filter_by(id=pid).first()
    db.session.delete(P)
   
    db.session.commit()

    return redirect(url_for('profile'))

    