from flask import Flask, render_template,request,redirect
import getResults
import redis
import os
from urllib.parse import urlparse
url = urlparse(os.environ.get("REDISCLOUD_URL"))
app = Flask(__name__)
myHostname = "asm.redis.cache.windows.net"
myPassword = os.environ.get("redis_pass")

r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
#r = redis.StrictRedis(host=myHostname, port=6380,
#                      password=myPassword, ssl=True)

#result = r.ping()



@app.route('/')
def home():
    print(r.delete('17BK1A05A8144217'))
    return render_template('home.html')

@app.route('/getlist',methods=['GET','POST'])
def index():
    tcount=0
    if request.method=="POST":
        a=request.form.get('start').upper()
        b=request.form.get('end').upper()
        ores = request.form.get('result')
        print("in post")
    elif request.args['start'] and request.args['end']:
        a = request.args['start'].upper()
        b = request.args['end'].upper()
        ores = request.args['result']
        print("in get")
    if request.method=="POST" or request.args['start'] and request.args['end']:
        if(a[0:8]!=b[0:8]):
            return render_template("home.html")
        res = ores.split(".")
        print(a)
        print(b)
        print(res)
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
             'J':8
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
        if(end-start<0 or end-start>210):
            return render_template('home.html')
        for i in range(start, end+1):
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
                elif i > 179 and i < 190:
                    ht=rollno + 'j' + str(i - 180)
                id=ht+res[0]+res[1]

                #############################SEARCHING IN DATABASE################################
                print(f"Checking {id} in Database....")
                if r.get('badht'+id):
                    print(f"{id} is wrong HTNO found in Database")
                    continue
                elif r.get(id):
                    print(f"{id} found in Database")
                    dict = str(r.get(id)).strip('b')
                    #print(dict)
                    y=str(eval(dict))
                    z=eval(y)
                    xcgpa = float(z[0])
                    xpersonalData = eval(z[1])
                    xmarksData = eval(z[2])
                #############################SEARCHING IN SERVER################################
                else:
                    print(f"Checking {id} in Server....")
                    student = getResults.getResultData()
                    check = student.run(ht, res[0], res[1])
                    if (check == "HT ERROR"):
                        print(f"{id}  not found in server")
                        r.set('badht'+id,'True')
                        continue
                    elif (check == "SERVER ERROR"):
                        tcount+=1
                        print("Server Error")
                        continue
                        render_template("home.html")
                    elif (check == True):
                        tcount+=1
                        print(f"{id} found on Server")
                        kcgpa = str(student.cgpa)
                        kpersonalData = str(student.personalData)
                        kmarksData = str(student.marksData)
                        s=f"""["{kcgpa}","{kpersonalData}","{kmarksData}"]"""
                        r.set(id,s)
                        xcgpa = student.cgpa
                        xpersonalData = student.personalData
                        xmarksData = student.marksData
                        print(tcount)
                        if(tcount>20):
                            url1='getlist?start='+a+'&end='+b+'&result='+ores
                            print(url1)
                            return redirect(url1)
                cgpalist.append(xcgpa)
                personalDatalist.append(xpersonalData)
                marksDatalist.append(xmarksData)
        if cgpalist==[] or marksDatalist==[] or personalDatalist==[]:
            return render_template("home.html")
        #print(cgpalist)
        #print(personalDatalist)
        #print(marksDatalist)
        tableHead=[]
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
