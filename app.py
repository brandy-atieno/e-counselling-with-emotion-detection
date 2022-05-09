from os import name
import os
from flask import Flask, render_template, abort, session, redirect,flash,request,url_for,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
from wtforms import Form,StringField,PasswordField,BooleanField, form
from wtforms import validators
from wtforms.validators import InputRequired,Email,DataRequired, ValidationError,length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin,LoginManager, login_manager,login_user,login_url,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


from flask_mail import Mail, Message
from config import mail_username, mail_password


# for the intelligence
import predict
import random
import string
import cv2


app = Flask(__name__)
bcrypt=Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/flask_blog"
app.config['SECRET_KEY'] = "mysecretkeywhichissupposedtobesecret"



db = SQLAlchemy(app)
admin = Admin(app)
bcrypt = Bcrypt(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(25),)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    phone=db.Column(db.String(10))
    password=db.Column(db.String(80))
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True

        else:
            abort(403)        

admin.add_view(SecureModelView(User, db.session))

class LoginForm(Form):
    username=StringField('username',validators=[InputRequired(),length(min=5,max=15)])
    password=PasswordField('password',validators=[InputRequired(),length(min=5,max=80)])
    remember=BooleanField('remember me')




class AdminForm(Form):
    username=StringField('username',validators=[InputRequired(),length(min=5,max=15)])
    password=PasswordField('password',validators=[InputRequired(),length(min=5,max=80)])
    remember=BooleanField('remember me')

class RegisterForm(Form):
    name=StringField('name',validators=[InputRequired(),length(min=5,max=15)])
    username=StringField('username',validators=[InputRequired(),length(min=5,max=15)])
    email=StringField('email',validators=[DataRequired('enter email')])
    phone=StringField('phone',validators=[DataRequired(),length(min=10,max=15)])
    password=PasswordField(' password',validators=[length(min=5,max=80),
    validators.EqualTo ('confirm',message='password must match')])
    confirm=PasswordField('Repeat Password',validators=[length(min=5,max=18)])
    
def validate_username (self,username):
         existing_user_username=User.query.filterby(username=username.data).first()
         if existing_user_username:
             raise ValidationError
             "Username already exists choose another"

@app.route('/userlog',methods=['GET','POST'])
def userlog():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if  bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)

                return redirect(url_for('new'))

        
        return '<h1> Invalid username or password<h1>'
                   
    
    return   render_template('userlog.html', form=form)

@app.route('/REGISTER',methods=['GET','POST'])
def REGISTER():
 form = RegisterForm(request.form)

 if request.method == 'POST' and form.validate:

  hashed_password=bcrypt.generate_password_hash(form.password.data)
  new_user=User(name=form.name.data,username=form.username.data,email=form.email.data,phone=form.phone.data,password=hashed_password)
  db.session.add(new_user)
  db.session.commit()
  return '<h1> SUCCESSFUL SIGN UP  <h1>'

 return  render_template('REGISTER.html', form = form)
    
@app.route('/new')
@login_required
def new():
    print('just checking')
    return  render_template('new.html',name=current_user.username)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime)
    slug = db.Column(db.String(255))

class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    frame=db.Column(db.String(255))
    status=db.Column(db.String(255))
    name=db.Column(db.String(255))
    date_posted = db.Column(db.DateTime)
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
    admin.add_view(SecureModelView(Predictions, db.session))
    

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)



admin.add_view(SecureModelView(Posts, db.session))
class StudentForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phone= db.Column(db.Integer)
    regno = db.Column(db.String(255))
    email = db.Column(db.String(255))
    isssue= db.Column(db.String(255))
    time= db.Column(db.String(255))
    channel= db.Column(db.String(255))

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


    admin.add_view(SecureModelView(StudentForm, db.session))
    

@app.route("/")
def index():
    posts = Posts.query.all()
    return render_template("index.html", posts=posts)



@app.route('/check_mood')
def check_mood():
    frame,status=predict.predict_mood()
    image_name=random_string_generator(25) + '.png'
    current_wdr = os.getcwd()
    working_dr = current_wdr + '\images'
    os.chdir(working_dr)
    cv2.imwrite(image_name ,frame)
    new_prediction=Predictions(frame=image_name,status=status,name=current_user.username)
    db.session.add(new_prediction)
    db.session.commit()
    os.chdir(r"C:\Users\Brandy Odhiambo\Documents\project\flask-blog-tutorial-master")
    return  render_template('new.html', name=current_user.username) 


def random_string_generator(str_size):
    chars = string.ascii_letters 
    return ''.join(random.choice(chars) for x in range(str_size))   






class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    category = db.Column(db.String(255))
    signs=db.Column(db.String(255))
    effect=db.Column(db.String(255))
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    admin.add_view(SecureModelView(Topics, db.session))
    

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/counsel")
def counsel():
    return render_template("counsel.html")

@app.route('/topics',methods=['GET','POST'])
def topics():
  if request.method == 'POST':
    return '<h1> Successful Filling  <h1>'

  return  render_template('topics.html', form = form)

    



@app.route("/post/<string:slug>")
def post(slug):
    try:
        post = Posts.query.filter_by(slug=slug).one()
        return render_template("post.html", post=post)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)

class ContanctDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    email= db.Column(db.String(255))
    phone=db.Column(db.Integer)
    message=db.Column(db.String(255))



@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        return render_template("contact.html")

    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"],)
def login ():
 form = AdminForm(request.form)  

 if request.method == "POST":
    if request.form.get("username") =="were" and request.form.get("password") == "123":
      session['logged_in'] = True
      return redirect("/admin")
    else:
        return render_template("login.html", failed=True)
 return render_template("login.html", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")



          
    #Save
    #send to the doctor    

    # When everything done, release the capture
    

    return (frame, status)




if __name__ == "__main__":
    app.run(debug=True)
