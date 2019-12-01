
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

# class L_Cam(threading.Thread):
#     def __init__(self, q, loop_time = 1.0/60):
#         self.q = q
#         self.timeout = loop_time
#         self.img = None
#         super(L_Cam, self).__init__()
    
#     def run(self):
#         while True:
#             try: 
#                 function, args, kwargs = self.q.get(timeout=self.timeout)
#                 function(*args, **kwargs)
#             except queue.Empty:
#                 self.idle

#     def idle(self):
#         while True:

#             img = l.image()
#             print(img)
#             self.img = img
#     # img_io = BytesIO()
    
#     # if img:  
#     def onThread(self, function, *args, **kwargs):
#         self.q.put((function, args, kwargs))

#     def gen(self):
#         print(self.img)
#         self.img.save(img_io, 'JPEG', quality=100)
#         stream = img_io
#         stream.seek(0)
#         frame = stream.read()
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def gen(img):
    
    img.save(img_io, 'JPEG', quality=100)
    stream = img_io
    stream.seek(0)
    frame = stream.read()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def gen(camera):
#     while True:
#         frame = camera
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
q = queue.Queue()
# t1 = threading.Thread(target=L_Cam(q), name=L_Cam(), args=(q,))
# t1.start()
t1 = L_Cam(q)

t1.start()



@app.route('/video_feed')
def video_feed():
    
    return Response(t1.onThread(t1.gen(), mimetype='multipart/x-mixed-replace; boundary=frame'))

# def serve_pil_image(pil_img):
#     print(pil_img)
#     img_io = BytesIO()
#     pil_img.save(img_io, 'JPEG', quality=100)
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/jpeg')


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     print(return_img())
#     return Response(return_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

def flaskServer():
    app.run(host="0.0.0.0", debug=False)

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


if __name__ == "__main__":
    global status
    

    thread = Thread(target=flaskServer)
    thread.start()
    sleep(2)
    signal.signal(signal.SIGINT, signal_handler)

