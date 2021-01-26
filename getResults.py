import bs4,requests;


class getResultData:

    def run(self,rollno,code,batch):
        try:
            if code=='1442' or code=='1437':
                link=f'http://results.jntuh.ac.in/results/resultAction?degree=btech&examCode={code}&etype=r{batch}&result=null&grad=null&type=intgrade&htno=' + rollno.upper()
                originalData = requests.get(link,timeout=5.0);
            else:
                originalData = requests.get(
                    f'http://202.63.105.184/results/resultAction?degree=btech&examCode={code}&etype=r{batch}&result=null&grad=null&type=grade{batch}&htno=' + rollno.upper(),timeout=2.0);
            print(originalData)
            parsedData = bs4.BeautifulSoup(originalData.text, 'html.parser')
            if "invalid hallticket number" in str(parsedData):
                return "HT ERROR"
            elif "Server Error" in str(parsedData):
                return "SERVER ERROR"
            else:
                self.backlogs = 0
                savedData = []
                for x in parsedData.find_all('td'):
                    savedData.append(
                        str(x).replace('<td>', '').replace('<b>', '').replace('</b>', '').replace('<h4>', '').replace('</td>',
                                                                                                                      '').replace(
                            '</h4', ''))
                for x in range(len(savedData)):
                    if "<td style" in savedData[x]:
                        end = x
                # print(end)
                savedData = savedData[0:end]
                personalData = {savedData[0]: savedData[1],
                                savedData[2]: savedData[3],
                                savedData[4]: savedData[5],
                                savedData[6]: savedData[7]
                                }
                # print(savedData)
                personalData = {savedData[0]: savedData[1],
                                savedData[2]: savedData[3],
                                savedData[4]: savedData[5],
                                savedData[6]: savedData[7]
                                }

                marksData = {}
                creditsData = {}
                #print(len(savedData))
                for x in range(16, end - 2, 7):
                    marksData[savedData[x]] = savedData[x + 4]
                    creditsData[savedData[x]] = savedData[x + 5]
                self.creditsData = creditsData
                self.marksData = marksData
                self.personalData = personalData
                print(personalData)
                print(marksData)
                print(creditsData)
                cgpa = 0
                points = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0, 'Ab': 0}
                self.totalcredits = 0;

                for x in self.creditsData:
                    self.totalcredits += float(self.creditsData[x])

                for x in self.marksData:
                    if (points[self.marksData[x]] == 0):
                        self.backlogs += 1
                        break
                    else:
                        cgpa += points[self.marksData[x]] * float(self.creditsData[x]) / self.totalcredits
                if (self.backlogs > 0):
                    self.cgpa = 0
                else:
                    self.cgpa = format(cgpa, '.2f')

                return True

        except:
            return "SERVER ERROR"




