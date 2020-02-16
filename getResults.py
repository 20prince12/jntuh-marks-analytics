import bs4,requests;


class getResultData:

    def __init__(self,rollno):
        print('test')
        originalData=requests.get('http://epayments.jntuh.ac.in/results/resultAction?degree=btech&examCode=1387&etype=r16&result=null&grad=null&type=grade16&htno='+rollno.upper());
        print('test')
        parsedData=bs4.BeautifulSoup(originalData.text,'html.parser')
        savedData=[]
        for x in parsedData.find_all('td'):
            savedData.append(str(x).replace('<td>','').replace('<b>','').replace('</b>','').replace('<h4>','').replace('</td>','').replace('</h4',''))

        personalData={savedData[0]:savedData[1],
                    savedData[2]:savedData[3],
                    savedData[4]:savedData[5],
                    savedData[6]:savedData[7]
                  }
        marksData={savedData[13]:savedData[14],
                    savedData[17]:savedData[18],
                    savedData[21]:savedData[22],
                    savedData[25]:savedData[26],
                    savedData[29]:savedData[30],
                    savedData[33]:savedData[34],
                    savedData[37]:savedData[38],
                    savedData[41]:savedData[42],
                    savedData[45]:savedData[46]
                    }
        creditsData={savedData[13]:savedData[15],
                    savedData[17]:savedData[19],
                    savedData[21]:savedData[23],
                    savedData[25]:savedData[27],
                    savedData[29]:savedData[31],
                    savedData[33]:savedData[35],
                    savedData[37]:savedData[39],
                    savedData[41]:savedData[43],
                    savedData[45]:savedData[47]
                    }
        self.creditsData=creditsData
        self.marksData=marksData
        self.personalData=personalData
        cgpa = 0
        points = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0}
        self.totalcredits = 0;
        for x in self.creditsData:
            self.totalcredits += int(self.creditsData[x])
        for x in self.marksData:
            if (points[self.marksData[x]] == 0):
                return 0
            cgpa += points[self.marksData[x]] * int(self.creditsData[x]) / self.totalcredits
        self.cgpa=format(cgpa,'.2f')