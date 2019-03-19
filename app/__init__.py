'''
    File name: __init__.py
    Author: Flynn Harrison
    Date created: 18/03/2019
    Python Tested Version: 3.7
'''

import os
from flask import Flask, render_template
from flask import request
from dateutil import parser
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import string
import random
import time

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
try:
    app.config.from_pyfile('config.py')
except IOError:
    pass

# Todo; impleament log line limit (remove old lines from temps.txt)
# Todo; api update call speed limit

# Folder check and create
def folder_check_create(folder):
    print('check dir '+folder)
    if os.path.isdir(folder):
        return True
    else:
        try:
            os.makedirs(folder)
        except OSError:
            print("Failed to create " +folder )
            return False
        return True

def time_diff(a, b):
    diff = b-a
    (mins, secs) = divmod(diff.days * 86400 + diff.seconds, 60)
    return (mins, secs)
    
# Checks if a key is currently valid.
# keys are defined if they have a dir in the data dir
def check_key(key=None):
    if key is not None:
        if os.path.isdir("data/"+str(key)):
            return key
        else:
            return None
    key = request.args.get("key", type = str)
    if os.path.isdir("data/"+str(key)):
        return key
    else:
        return None

def key_gen(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.before_first_request
def startup():
    folder_check_create('data')
    folder_check_create('app/static/')

@app.route('/getkey')
def get_key():
    # Maybe better way to give the user a key.
    # also this could be abused, this needs to be addressed 
    while True:
        key = key_gen()
        print('key:'+key)
        if check_key(key) is None:
            os.mkdir("data/"+key)
            return key

@app.route('/update')
def home():
    # Check key
    key = check_key()
    if key is None:
        return 'Invalid Key'

    # Check temp
    temp = request.args.get('temp')
    if temp is None:
        return 'Invalid temp'

    # Recorde Data
    time = datetime.datetime.now()
    with open("data/"+key+"/temps.txt", "a+") as f:
        f.write(("%s, %s\n") % (time, temp))
    return 'Succesfully tracked'

@app.route('/remove/<name>')
def remove(name):
    # Check key
    key = check_key()
    if key is None:
        return 'Invalid Key'

    # Remove key option
    if name is 'key':
        os.removedirs('data/'+key)
        return 'Removed key and associated data'

    # Remove log file
    if name is 'log':
        if os.path.isfile("data/"+key+"/temps.txt"):
            os.remove("data/"+key+"/temps.txt")
        return 'Removed log'
    
    # name was not valid
    return 'Not valid remove'

@app.route('/')
def temp():
    # Check key
    key = check_key()
    if key is None:
        return 'Invalid Key'

    # Open file
    # file check
    if not os.path.isfile("data/"+key+"/temps.txt"):
        open("data/"+key+"/temps.txt", 'w+')
        return 'empty data set'

    # Read content
    with open("data/"+key+"/temps.txt", 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    last_time = parser.parse(last_line.split(',')[0])
    temp = last_line.split(',')[1]
    current_time = datetime.datetime.now()
    (mins, secs) = time_diff(last_time, current_time)
    x = [-time_diff(parser.parse(line.split(',')[0]), current_time)[0]
         for line in lines]
    y = [float(line.split(',')[1]) for line in lines]

    # Remove any old graph
    for file in os.scandir('app/static/'):
        if file.name.endswith(".png"):
            os.remove(file.path)

    # Plot figure
    plot_name = key_gen()
    plt.figure()
    plt.ylim(0, 45)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title("Temperature Vs Time")
    plt.plot(x, y, 'rH:')
    plt.savefig('app/static/'+plot_name+'.png')
    return render_template('temp.html', mins=mins, secs=secs, temp=temp, plot_name = plot_name)

