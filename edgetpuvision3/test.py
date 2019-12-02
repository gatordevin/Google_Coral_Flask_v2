from flask import Flask, render_template, url_for, copy_current_request_context, Response
from random import random
from time import sleep
import queue
from apps3 import Run_Server
import logging
import itertools
from PIL import Image
from io import BytesIO
from threading import Thread, active_count, Event
import sys
import threading
from classify import Model
from detect import Model_Detect
from flask import Flask, Response, redirect, request, url_for
__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0





class DataStore():
    a = None
    c = None

data = DataStore()




model = Model
    
data.a = Run_Server(model)


def checkClient(q, qu):
    while True:

        img = data.a.image()[0]
        svg = data.a.image()[1]
        # print(svg)
        if svg:
            qu.put(svg)
        if img:
            q.put(img)
        sleep(.001)

q = queue.Queue(maxsize=2)
qu = queue.Queue(maxsize=2)
t1 = threading.Thread(target=checkClient, name=checkClient, args=(q, qu))

t1.start()
t1.deamon = True


def svg():
    for i, c in enumerate(itertools.cycle('\|/-')):
        
        c = svg = qu.get()
        
        yield "data: %s \n\n" % (c)
def gen():
    while True:
        img = q.get()
        sleep(.01)
        if img:
            img_io = BytesIO()
            img.save(img_io, 'JPEG', quality=100)
            stream = img_io
            stream.seek(0)
            frame = stream.read()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        return Response(svg(), content_type='text/event-stream')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)