from flask import Flask, render_template,request
import getResults
from flask_mysqldb import MySQL



app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'asm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getlist',methods=['GET','POST'])
def index():

    if request.method=="POST":
        a=request.form.get('start').upper()
        b=request.form.get('end').upper()
        res=request.form.get('result').split(".")
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
        #print(start)
        #print(end)
        if(end-start<0 or end-start>180):
            return render_template('home.html')
        for i in range(start, end+1):
            try:
                if (i < 10):
                    ht=rollno + '0' + str(i)
                elif (i < 100):
                    ht=rollno + str(i)
                elif i > 99 and i < 110:
                    ht=rollno + 'A' + str(i - 100)
                elif i > 109 and i < 120:
                    ht=rollno + 'B' + str(i - 110)
                elif i > 119 and i < 130:
                    ht=rollno + 'C' + str(i - 120)
                    student = getResults.getResultData(ht, res[0], res[1])
                elif i > 129 and i < 140:
                    ht=rollno + 'D' + str(i - 130)
                elif i > 139 and i < 150:
                    ht=rollno + 'E' + str(i - 140)
                elif i > 149 and i < 160:
                    ht=rollno + 'F' + str(i - 150)
                elif i > 159 and i < 170:
                    ht=rollno + 'G' + str(i - 160)
                elif i > 169 and i < 180:
                    ht=rollno + 'H' + str(i - 170)
                id=ht+res[0]+res[1]
                curs = mysql.connection.cursor()
                print("test")
                if curs.execute("SELECT * FROM data WHERE id=%s", [id]) >= 1:
                    print(id)
                    curs.execute("SELECT * FROM data WHERE id=%s", ['17BK1A05A7138716'])  # id level info
                    dict = curs.fetchone()
                    xcgpa=int(dict['cgpa'])

                    xpersonalData=dict['personalData']
                    xmarksData=dict['marksData']
                else:
                    student = getResults.getResultData(ht, res[0], res[1])
                    curs.execute("INSERT INTO data(id, cgpa, personalData, marksData) VALUES(%s, %s, %s, %s)",
                             (id, student.cgpa, student.personalData, student.marksData))
                    xcgpa=student.cgpa
                    xpersonalData=student.personalData
                    xmarksData=student.marksData
                print("test3")
                cgpalist.append(xcgpa)
                personalDatalist.append(xpersonalData)
                marksDatalist.append(xmarksData)
            except:
                print("none found")
        #print(cgpalist)
        #print(personalDatalist)
        #print(marksDatalist)
        tableHead=[]
        passed=0
        failed=0
        tableHead.append("Roll.No")
        tableHead.append("Name")
        tableHead.append("CGPA")
        for x in marksDatalist[0]:
            tableHead.append(x)

        tableData=[]
        for  x  in range(len(personalDatalist)):
            tableData.append([])
            tableData[x].append(personalDatalist[x]['HTNO:'])
            tableData[x].append(personalDatalist[x]['NAME:'])
        count=0
        for y in marksDatalist:
            tableData[count].append(cgpalist[count])
            for k in y:
                tableData[count].append(y[k])
            count += 1
        #print(tableData)
        #print(tableHead)
        failed=cgpalist.count(0)
        passed=len(cgpalist)-failed
        #print(passed)
        #print(failed)
        passper=format(((passed/(passed+failed))*100),'.2f')
        failper=format(((failed/(passed+failed))*100),'.2f')
        #print(passper)
        #print(failper)

        return render_template('getlist.html',cgpalist=cgpalist,tableHead=tableHead,tableData=tableData,tableheadLen=len(tableHead),tableDatalen=len(tableData),passper=passper,failper=failper)
    return render_template('home.html')
