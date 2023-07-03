import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 网站URL和目标邮箱地址
url = 'https://luzmod.com/#beginner-friendly'
to_addr = 'lilyyang950901@gmail.com'

# Gmail帐户名和密码
gmail_user = 'lilyyang950901@gmail.com'
gmail_password = '199591yyz'

# 获取HTML内容
response = requests.get(url)
html = response.content

# 解析HTML并获取每周workout计划
soup = BeautifulSoup(html, 'html.parser')
weeks = soup.find_all('div', {'class': 'col-md-6'})

# 创建日历事件
cal = Calendar()
cal.add('prodid', '-//My calendar//example.com//')
cal.add('version', '2.0')

# 计算本周Monday和Sunday的日期
today = datetime.today()
monday = today - timedelta(days=today.weekday())
sunday = monday + timedelta(days=6)

# 遍历每周计划，创建事件并添加到日历中
for week in weeks:
    days = week.find_all('div', {'class': 'col-md-1'})
    exercises = week.find_all('div', {'class': 'col-md-5'})

    for day, exercise in zip(days, exercises):
        date = monday + timedelta(days=int(day.text)-1)
        start_time = datetime.combine(date, datetime.min.time())
        end_time = start_time + timedelta(hours=1)

        event = Event()
        event.add('summary', f'Workout: {exercise.text}')
        event.add('dtstart', start_time)
        event.add('dtend', end_time)
        event.add('dtstamp', datetime.now())
        event['uid'] = f'{date.strftime("%Y%m%d")}T{start_time.strftime("%H%M%S")}'

        cal.add_component(event)

# 将日历事件保存到文件
with open('workout.ics', 'wb') as f:
    f.write(cal.to_ical())

# 发送电子邮件
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to_addr
msg['Subject'] = f'Workout Plan ({monday.strftime("%m/%d/%Y")} - {sunday.strftime("%m/%d/%Y")})'

body = MIMEText(f'Please find attached workout plan for the week of {monday.strftime("%m/%d/%Y")} - {sunday.strftime("%m/%d/%Y")}).')
msg.attach(body)

with open('workout.ics', 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='ics')
    attachment.add_header('Content-Disposition', 'attachment', filename='workout.ics')
    msg.attach(attachment)

smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_server.login(gmail_user, gmail_password)
smtp_server.sendmail(gmail_user, to_addr, msg.as_string())
smtp_server.quit()