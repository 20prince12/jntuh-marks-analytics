import bs4,requests;


class getResultData:

    def __init__(self,rollno,code,batch):
        self.backlogs=0
        originalData=requests.get(f'http://epayments.jntuh.ac.in/results/resultAction?degree=btech&examCode={code}&etype=r{batch}&result=null&grad=null&type=grade{batch}&htno='+rollno.upper());

        parsedData=bs4.BeautifulSoup(originalData.text,'html.parser')
        savedData=[]
        for x in parsedData.find_all('td'):
            savedData.append(str(x).replace('<td>','').replace('<b>','').replace('</b>','').replace('<h4>','').replace('</td>','').replace('</h4',''))
        savedData=savedData[0:48]
        personalData={savedData[0]:savedData[1],
                    savedData[2]:savedData[3],
                    savedData[4]:savedData[5],
                    savedData[6]:savedData[7]
                  }
        #print(savedData)
        personalData = {savedData[0]: savedData[1],
                        savedData[2]: savedData[3],
                        savedData[4]: savedData[5],
                        savedData[6]: savedData[7]
                        }

        marksData = {}
        creditsData = {}
        print(len(savedData))
        for x in range(13,46,4):
            marksData[savedData[x]]=savedData[x+1]
            creditsData[savedData[x]]=savedData[x+2]
        self.creditsData = creditsData
        self.marksData = marksData
        self.personalData = personalData
        #print(marksData)
        #print(creditsData)
        cgpa = 0
        points = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0}
        self.totalcredits = 0;
        for x in self.creditsData:
            self.totalcredits += int(self.creditsData[x])
        for x in self.marksData:
            if (points[self.marksData[x]] == 0):
                self.backlogs+=1
                break
            else:
                cgpa += points[self.marksData[x]] * int(self.creditsData[x]) / self.totalcredits
        if(self.backlogs>0):
            self.cgpa=0
        else:
            self.cgpa=format(cgpa,'.2f')
