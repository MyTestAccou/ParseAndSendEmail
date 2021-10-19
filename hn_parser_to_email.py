import requests 

from bs4 import BeautifulSoup 

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
now = datetime.datetime.now()


data_for_email = ''

# if you want scrype another site config this func 

def extract_news(url):
    print('Extracting Hacker News Stories ...')
    content = ''
    content +=('<br>HN Top Stories:</br>\n' + '<br>' + '-' * 50 +'<br>')
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs = {'class' : 'title', 'valign' : ''})):
        content += (str(i + 1) + ' :: ' + tag.text + "\n" + '<br>')
                

    return content

result_cont = extract_news('https://news.ycombinator.com/')

data_for_email += result_cont
data_for_email += ('<br>------------</br>')
data_for_email += ('<br></br>End Message')


print('Composing Emails')


# update your email details 


SERVER = 'smtp.gmail.com' # your smtp server
POST = 587 # enter port 
FROM = '' # enter you email addr 
TO = '' # enter who consume email its may be a list of addr 
PASS = '' # you email pass 

msg = MIMEMultipart()
# if you want another topics on your mass config it here 
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)

msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(data_for_email, 'html'))

print('Initiating Server')


server = smtplib.SMTP(SERVER, POST)

server.set_debuglevel(1) # if you want see error masg 1 or not 0
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent....')

server.quit()

