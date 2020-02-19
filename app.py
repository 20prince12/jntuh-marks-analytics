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
    if 1:
        start=request.form.get('start')
        end=request.form.get('end')
        cgpalist=[]
        creditsDatalist=[]
        personalDatalist=[]
        marksDatalist=[]
        rollno = "17BK1A05"

        for i in range(105, 109):
            try:
                if (i < 10):
                    ht=rollno + '0' + str(i)
                    student = getResults.getResultData(ht)
                elif (i < 100):
                    ht=rollno + str(i)
                elif i > 99 and i < 110:
                    ht=rollno + 'A' + str(i - 100)
                    student = getResults.getResultData(ht)
                elif i > 109 and i < 120:
                    ht=rollno + 'B' + str(i - 110)
                    student = getResults.getResultData(ht)
                cgpalist.append(student.cgpa)
                personalDatalist.append(student.personalData)
                marksDatalist.append(student.marksData)
            except:
                print("none found")
        #print(cgpalist)
        #print(personalDatalist)
        #print(marksDatalist)
        tableHead=[]
        tableHead.append("Name")
        for x in marksDatalist[0]:
            tableHead.append(x)
        tableHead.append("cgpa")
        tableData=[]
        for  x  in range(len(personalDatalist)):
            tableData.append([])
            tableData[x].append(personalDatalist[x]['NAME:'])
        for y in marksDatalist:
            for k in y:
                tableData[y].append(y[k])
        print(tableData)
        print(tableHead)
        return render_template('getlist.html',cgpalist=cgpalist,tableHead=tableHead,tableData=tableData)
    return render_template('getlist.html')
