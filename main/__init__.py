import os
from flask import Flask, render_template
from flask import request
from dateutil import parser
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np

app = Flask(__name__)

@app.route('/getkey')
def get_key():
    # Impleament a key gen

@app.route('/update')
def home():
    # Check key
    key = request.args.get('key')
    if not os.path.isdir('data/'+key):
        # implemeant check key list
        return "Invalid key"
    # Check temp
    temp = request.args.get('temp')
    if temp is None:
        return 'Invalid temp'
    time = datetime.datetime.now()
    with open("data/temps.txt", "a+") as f:
        f.write(("%s, %s\n") % (time, temp))
    return 'Succesfully tracked'

@app.route('/remove')
def remove():
    if os.path.isfile('data/temps.txt'):
        os.remove('data/temps.txt')
    return 'Removed log'


def time_diff(a, b):
    diff = b-a
    (mins, secs) = divmod(diff.days * 86400 + diff.seconds, 60)
    return (mins, secs)


@app.route('/')
def temp():
    with open('data/temps.txt', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    last_time = parser.parse(last_line.split(',')[0])
    temp = last_line.split(',')[1]
    current_time = datetime.datetime.now()
    (mins, secs) = time_diff(last_time, current_time)
    x = [-time_diff(parser.parse(line.split(',')[0]), current_time)[0]
         for line in lines]
    y = [float(line.split(',')[1]) for line in lines]
    plt.figure()
    plt.ylim(0, 45)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title("Flynn's Temperature Thing")
    plt.plot(x, y, 'rH:')
    plt.savefig('main/static/temp.png')
    return render_template('temp.html', mins=mins, secs=secs)
