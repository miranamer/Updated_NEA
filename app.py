from flask import Flask, render_template
from flask.templating import render_template_string
from flask import request, redirect
import pickle
import numpy as np
import math


# This is the diabetes model that makes a prediction
diab_model = pickle.load(open('diabetes.pkl', 'rb'))
heart_model = pickle.load(open('heart.pkl', 'rb'))


app = Flask(__name__)


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


# DELETE THIS COMMENT BELOW IT WILL MESS YOU OVER IN THE FINAL PRODUCT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Wrap the diabetes form in the same style as the heart disease form (first take a pic of crappy form for the report then change it )

# Add LINKS TO THE IMAGES IN THE ABOUT PAGE1

@app.route('/testpage')
def testpage():
    return render_template('testpage.html')



@app.route('/testpage2')
def testpage2():
    return render_template('testpage2.html')




if __name__ == '__main__':
    app.run(debug=True)