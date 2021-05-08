from __future__ import print_function
import os
from dotenv import load_dotenv
import csv
import urllib.request
from io import StringIO
from datetime import datetime
from dateutil import tz
import requests

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')

def timeNow():
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Bangkok')
    utc = datetime.utcnow()
    convert = utc.replace(tzinfo=from_zone).astimezone(to_zone)
    return convert.strftime('%d/%m/%Y %H:%M')

def linenotify(message):
    url = 'https://notify-api.line.me/api/notify'
    token = LINE_NOTIFY_TOKEN
    header = {'Authorization':'Bearer '+token}
    data = {'message':message}
    r = requests.post(url, headers=header, data=data)
    
def main():
    url = 'https://docs.google.com/spreadsheets/d/{}/export?gid=0&format=csv'.format(SPREADSHEET_ID)

    response = urllib.request.urlopen(url)
    
    f = StringIO(response.read().decode('utf-8'))
    data = list(csv.reader(f, delimiter=','))

    print(data[1:])
    message = '\n🌷สถิติเฝ้าเดี่ยวทีมนมัสการประจำสัปดาห์\n\n'
    for member in data[1:]:
        day = '-' if (int(member[8]) < 1) else member[8]
        message += '{} {} วัน\n'.format(member[0], day)

    message += '\n[อัปเดต {}]'.format(timeNow())
    message += '\n🪴ดูตารางแบบเต็มได้ที่ https://docs.google.com/spreadsheets/d/{}/view'.format(SPREADSHEET_ID)
    print(message)
    linenotify(message)

if __name__ == '__main__':
    main()