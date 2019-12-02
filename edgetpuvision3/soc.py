from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, Response
from random import random
from time import sleep
from threading import Thread, Event
from classify import Model
import queue
import threading
from apps3 import Run_Server

from apps3 import Run_Server
from threading import Thread, Event
from flask import Flask, send_file, Response, render_template
from time import sleep
from PIL import Image
from io import BytesIO
from threading import Thread, active_count
import signal
from threading import Thread, Event
from threading import Thread
import sys
import threading
import queue
from classify import Model


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0





model = Model

l = Run_Server(model)



def checkClient(q):
    while True:

        img = l.image()[0]
        svg = l.image()[1]

        
        q.put(img)
        qu.put(svg)
        sleep(.01)

q = queue.Queue(maxsize=2)
qu = queue.Queue(maxsize=2)
t1 = threading.Thread(target=checkClient, name=checkClient, args=(q,))
t1.start()
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

def svg():
    while True:
        svg = qu.get()
        
        if svg:
            return (svg)



#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        # number = round(random()*10, 3)
        number = svg()
        # print(number, "done")
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(.1)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('sanic.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@app.route('/video_feed')
def video_feed():
    
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')



@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=False)