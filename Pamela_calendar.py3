gmail_user = "lilyproductive@yahoo.com"
gmail_password = "s2u5v!H?!x*A7GH"

import datetime
from ics import Calendar, Event
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 定义计划表
schedule = {
    "Monday": "10 MIN LOWER AB WORKOUT",
    "Tuesday": "10 MIN BOMBASTIC BOOTY",
    "Wednesday": "12 MIN SLOW AB WORKOUT",
    "Thursday": "10 MIN YOGA FLOW",
    "Friday": "LIGHT SWITCH - Charlie Puth / Happy Dance Warm Up",
    "Saturday": "12 MIN SLOW AB WORKOUT",
    "Sunday": "REST DAY"
}

# 定义开始日期和持续时间
start_date = datetime.datetime.now().date()
duration = datetime.timedelta(weeks=4)

# 创建日历
cal = Calendar()

# 创建事件
for i in range(1, 29):
    for day, workout in schedule.items():
        # 每天香港时间早上9点开始锻炼
        local_start_time = datetime.datetime.combine(start_date + datetime.timedelta(days=i-1), datetime.time(hour=9))
        hongkong_offset = datetime.timedelta(hours=8)
        start_time = local_start_time - hongkong_offset
        end_time = start_time + datetime.timedelta(minutes=10)
        if day == datetime.datetime.strftime(local_start_time, "%A"):
            e = Event()
            e.name = workout
            e.begin = start_time
            e.end = end_time
            cal.events.add(e)

# 将日历写入ICS文件
with open("workout_schedule.ics", "w") as f:
    f.write(str(cal))


msg = MIMEMultipart()
msg['Subject'] = 'Workout Schedule'
msg['From'] = gmail_user
msg['To'] = 'lilyyang950901@gmail.com'

with open('workout_schedule.ics', 'rb') as f:
    part = MIMEApplication(f.read(), Name="workout_schedule.ics")
    part['Content-Disposition'] = 'attachment; filename="workout_schedule.ics"'
    msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(gmail_user, gmail_password)
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()

# 删除ICS文件
os.remove("workout_schedule.ics")