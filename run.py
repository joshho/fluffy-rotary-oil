import requests,re,os
import smtplib, ssl
from datetime import datetime, date

EMAIL=os.environ['EMAIL']
PASSWORD=os.environ['PASS']
SERVER=os.environ['SERVER']
PORT=os.environ['PORT']

pattern = 'Offer ends [0-9][0-9]/[0-9][0-9]/[0-9][0-9]'

URL = 'https://www.pennzoil.com/en_ca/promotions/do-it-yourself-oil-change.html'
page = requests.get(URL)

decoded=page.content.decode('utf-8')
result = re.findall(pattern, decoded)

foundRebate = 0
if result:
  #print(result)
  cur_date = datetime.now()
  for i in result:
    patternDate='[0-9][0-9]/[0-9][0-9]/[0-9][0-9]'
    resultDate = re.findall(patternDate, i)

    converted_date = datetime.strptime(resultDate[0], '%m/%d/%y')
    print("today: ",cur_date)
    print("found: ",converted_date.date())
    print(converted_date-cur_date)
    if (converted_date > cur_date):
        print("found")
        foundRebate = 1
        server = smtplib.SMTP(SERVER,PORT)
        server.starttls()
        server.login(EMAIL, PASS)
        server.sendmail(EMAIL, EMAIL, resultDate[0])
        server.quit()
    else:
        print("expired")
        server = smtplib.SMTP(SERVER,PORT)
        server.starttls()
        server.login(EMAIL, PASS)
        server.sendmail(EMAIL, EMAIL, resultDate[0])
        server.quit()
else:
  print("Search unsuccessful.")	
