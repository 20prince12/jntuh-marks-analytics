from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import getResults;

app = Flask(__name__)




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

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        a=request.form.get('start').upper()
        b=request.form.get('end').upper()
        cgpalist=[]
        personalDatalist=[]
        marksDatalist=[]
        d = {'A': 0,
             'B': 1,
             'C': 2,
             'D': 3,
             'E': 4,
             'F': 5,
             'G': 6,
             'H': 7,
             }
        rollno =a[0:8]
        s1 = str(a[8:10])
        s2 = str(b[8:10])
        def test(s1):
            try:

                s1 = int(s1)
                return s1
            except:
                s1 = str(d[s1[0]]) + str(s1[1])
                s1 = 100 + int(s1)
            return s1

        start = test(s1)
        end = test(s2)
        print(start)
        print(end)
        for i in range(start, end+1):
            try:
                if (i < 10):
                    ht=rollno + '0' + str(i)
                    student = getResults.getResultData(ht)
                elif (i < 100):
                    ht=rollno + str(i)
                    student = getResults.getResultData(ht)
                elif i > 99 and i < 110:
                    ht=rollno + 'A' + str(i - 100)
                    student = getResults.getResultData(ht)
                elif i > 109 and i < 120:
                    ht=rollno + 'B' + str(i - 110)
                    student = getResults.getResultData(ht)
                elif i > 119 and i < 130:
                    ht=rollno + 'C' + str(i - 120)
                    student = getResults.getResultData(ht)
                elif i > 129 and i < 140:
                    ht=rollno + 'D' + str(i - 130)
                    student = getResults.getResultData(ht)
                elif i > 139 and i < 150:
                    ht=rollno + 'E' + str(i - 140)
                    student = getResults.getResultData(ht)
                elif i > 149 and i < 160:
                    ht=rollno + 'F' + str(i - 150)
                    student = getResults.getResultData(ht)
                elif i > 159 and i < 170:
                    ht=rollno + 'G' + str(i - 160)
                    student = getResults.getResultData(ht)
                elif i > 169 and i < 180:
                    ht=rollno + 'H' + str(i - 170)
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
        tableHead.append("Roll.No")
        tableHead.append("Name")
        for x in marksDatalist[0]:
            tableHead.append(x)
        tableHead.append("cgpa")
        tableData=[]
        for  x  in range(len(personalDatalist)):
            tableData.append([])
            tableData[x].append(personalDatalist[x]['HTNO:'])
            tableData[x].append(personalDatalist[x]['NAME:'])
        count=0
        for y in marksDatalist:
            for k in y:
                tableData[count].append(y[k])
            tableData[count].append(cgpalist[count])
            count += 1
        print(tableData)
        print(tableHead)
        return render_template('getlist.html',cgpalist=cgpalist,tableHead=tableHead,tableData=tableData,tableheadLen=len(tableHead),tableDatalen=len(tableData))
    return render_template('getlist.html')
