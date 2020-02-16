from flask_mysqldb import MySQL
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import getResults;

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/calculate', methods=['GET','POST'])
def calculate():
    if request.method == 'POST':
        roll=request.form.get('roll')
        try:
            student=getResults.getResultData(roll)
            print(student.cgpa)
            print(student.creditsData)
            print(student.personalData)
            print(student.marksData)
        except:
            return render_template('cgpa.html', x='Server Error or Invalid HT no')
        return render_template('cgpa.html',x=student.cgpa)
    else:
        return render_template('cgpa.html')