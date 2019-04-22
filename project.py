from flask import Flask, render_template, request, redirect, \
jsonify, url_for, flash
import json
from flask import make_response
import urllib.parse
from time import mktime
import time
import datetime
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users

app = Flask(__name__)
APPLICATION_NAME = "MedReminder Application"

engine = create_engine('sqlite:///medreminder.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#Project apiKey textlocal : noPQi7NR1iM-nVwcv6gHFGzrTS40szTX3MpjZHDaEI
@app.route('/', methods=['GET','POST'])
def MedReminder():
    global request
    if request.method == 'POST':
        name = request.form['name']
        number = '91' #Only India Supported
        number += request.form['number']
        detail = request.form['detail']
        email = request.form['email']
        age = request.form['age']
        sender = 'TXTLCL'
        time = request.form['schedule_time']
        message = 'Reminder : ' + detail + ' - The MedReminder Team.'
        timeX = datetime.datetime.strptime(time, "%m/%d/%Y %I:%M %p").timetuple()
        unixtime = mktime(timeX)
        if number.isdigit() and len(number) == 12 and len(detail) > 5 and len(name) > 1 and int(age) > 0 and int(age) < 100:
            user = Users(name=name, email=email, age=age, detail=detail, number=number)
            session.add(user)
            session.commit()
            data =  urllib.parse.urlencode({'apiKey': 'noPQi7NR1iM-nVwcv6gHFGzrTS40szTX3MpjZHDaEI', 'numbers': number,
                'message' : message, 'sender': sender, 'schedule_time' : unixtime})
            data = data.encode('utf-8')
            request = urllib.request.Request("http://api.textlocal.in/send/?")
            f = urllib.request.urlopen(request, data)
            fr = f.read()
            print('--- Debug Statement ---  \n')
            print (fr)
            print('--- EO Debug Statement --- \n')
            return render_template('index.html', flash = 'Successfully Registered!', flashType = 'success')
        else :
            return render_template('index.html', flash = 'Incorrect Details. Please retry.', flashType = 'danger')
    else :
        return render_template('index.html', flash = None)

@app.route('/display', methods=['GET'])
def Display():
    users = session.query(Users).all()
    return render_template('display_users.html', users=users)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key_bro'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
