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
            return render_template('cgpa.html', x='Server Error or Invalid HT')
        return render_template('cgpa.html',x=student.cgpa,y=student.backlogs)
    else:
        return render_template('cgpa.html')

@app.route('/getlist', methods=['GET','POST'])
def getlist():
    if request.method == 'POST':
        start=request.form.get('start')
        end=request.form.get('end')
        cgpa=[]
        for x in range(60,100):
            roll='17bk1a05'+str(x)
            try:
                student = getResults.getResultData(roll)
                cgpa.append(student.cgpa)
                #print(student.creditsData)
                #print(student.personalData)
                #print(student.marksData)
            except:
                print("invalid ht no")
        return render_template('getlist.html', cgpa=cgpa)
    return render_template('getlist.html')
