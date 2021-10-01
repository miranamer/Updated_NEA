from enum import unique
from flask import Flask, render_template, url_for, flash
from flask.templating import render_template_string
from flask import request, redirect
import pickle
from flask_wtf.recaptcha import validators
import numpy as np
import math
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt




# This is the diabetes model that makes a prediction
diab_model = pickle.load(open('diabetes.pkl', 'rb'))
heart_model = pickle.load(open('heart.pkl', 'rb'))


app = Flask(__name__)




db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("Username Already Taken")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diabetes_pre')
def diabetes_pre():
    return render_template('diabetes_page.html')



@app.route('/diabetes', methods=['POST', 'GET'])
def diabetes():
    
    if request.method == "POST":

        req = request.form
        
        Pregnancies = req["Pregnancies"]
        Glucose = req["Glucose"]
        BloodPressure = req["BloodPressure"]
        SkinThickness = req["SkinThickness"]
        Insulin = req["Insulin"]
        BMI = req["BMI"]
        DiabetesPedigreeFunction = req["DiabetesPedigreeFunction"]
        Age = req["Age"]

        arr = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        pred = diab_model.predict(arr)
        pred = np.round(pred[0], 2) * 100
        significant_digits = 3
        pred = round(pred, significant_digits - int(math.floor(math.log10(abs(pred)))) - 1)
        
        
        
        output = pred

        return render_template('diabetes_after.html', output=output)
        
        
@app.route('/about')
def about():
    return render_template('about.html')


# NOT REALLY NEEDED
@app.route('/background_test')
def background_test():
    return render_template('background_test.html')






@app.route('/heart_disease_test_before')
def heart_disease_test_before():
    return render_template('form_test.html')




@app.route('/heart_disease_test_after', methods=['POST', 'GET'])
def heart_disease_test_after():

    if request.method == "POST":

        req = request.form
        
        age = req["age"]
        sex = req["sex"]
        cp = req["cp"]
        trestbps = req["trestbps"]
        chol = req["chol"]
        fbs = req["fbs"]
        restecg = req["restecg"]

        thalac = 220 - int(age)

        arr = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalac, 0, 2.3, 0, 0, 1]])
        pred = heart_model.predict(arr)
        pred = pred[0]
        output = pred


        return render_template('heart_disease_after.html', output=output)

# Create a help page here --> This provides info for the heart disease ai

@app.route('/heart_help')
def heart_help():
    return render_template('heart_help.html')


# Create a help page for the diabetes ai
@app.route('/diabetes_help')
def diabetes_help():
    return render_template('diabetes_help.html')
    

    
    
# Create a login page and a sign up page using SQL

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('login'))
        
            else:
                flash('Incorrect Login')
                return redirect(url_for('login'))

        



            




    return render_template('login.html', form=form)




@app.route('/logout')
@login_required
def logout():
    flash('Logged Out! - See You Again')
    return redirect(url_for('login'))

@app.route('/success_login')
@login_required
def success_login():
    return render_template('success_login.html')


@app.route('/unsuccessful_login')
def unsuccessful_login():
    return render_template('unsuccessful_login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created!')
        return redirect(url_for('login'))

    #else:
       # flash('Something Went Wrong!')
       # return redirect(url_for('login'))

    #message1 = 'User Already Taken!'

    return render_template('signup.html', form=form)



# Wrap the diabetes form in the same style as the heart disease form

# Add LINKS TO THE IMAGES IN THE ABOUT PAGE1

@app.route('/testpage')
def testpage():
    return render_template('testpage.html')



@app.route('/testpage2')
def testpage2():
    return render_template('testpage2.html')




if __name__ == '__main__':
    app.run(debug=True)