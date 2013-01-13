from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

DEPARTURES_URL = 'http://ojp.nationalrail.co.uk/service/ldbboard/dep/BCV/LST/To'

def get_next_departure():
    r = requests.get(DEPARTURES_URL)
    data = BeautifulSoup(r.content)
    row = data.select(".firstRow")
    status = 'None'
    next_train = None
    if row:
        hour, minute = row[0].td.string.split(':')
        next_train = datetime.combine(date.today(), time(int(hour), int(minute)))
        status = row[0].select('.status')[0].string
    return next_train, status

@app.route('/')
def index():
    # get next train time
    next_train, status = get_next_departure()
    if next_train:
        time_to = relativedelta(next_train, datetime.now())
        time_of = next_train.strftime('%H:%M')
        minutes_to = time_to.minutes
    else:
        minutes_to = '0'
        time_of = 'No train'
        
    return render_template('index.html', 
                           train_time=time_of,
                           minutes_to=minutes_to,
                           status=status)

if __name__ == '__main__':
    app.run()
