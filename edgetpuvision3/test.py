import queue
import threading
import requests

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

app = Flask(__name__)


model = Model

l = Run_Server(model)



def checkClient(q):
    while True:

        img = l.image()[0]
        svg = l.image()[1]

        
        q.put(img)
        sleep(.01)

q = queue.Queue(maxsize=2)
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
        img = q.get()
        
        if img:
            yield (img)



# from flask import stream_with_context, request, Response

# @app.route('/stream')
# def streamed_response():
#     def generate():
#         yield 'Hello '
#         yield 'yeee'
#         yield '!'
#     return Response(stream_with_context(next(svg())))



@app.route('/video_feed')
def video_feed():
    
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# custom_color_global_variable = 'red'

# @app.route('/circle-thin-custom-color.svg', methods=('GET', 'HEAD'))
# def circle_thin_custom_color():
#     """Thin circle with the color set by a global variable."""
    
#     return Response(svg(),
#         mimetype='image/svg+xml'
#    )

@app.route('/')
def index():
    return render_template('index.html')



def flaskServer():
    app.run(host="0.0.0.0", debug=False)

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


if __name__ == "__main__":
    global status
    
    thread22 = Thread(target=gen)
    thread22.start()
    thread22.deamon = True
    thread = Thread(target=flaskServer)
    thread.start()
    sleep(2)
    signal.signal(signal.SIGINT, signal_handler)




# while True:
#     value = q.get()
#     print(value)
#     sleep(.01)