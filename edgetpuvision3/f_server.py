
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
from classify import Model

app = Flask(__name__)


model = Model

l = Run_Server(model)


def return_img():
  while True:

    img = l.image()
    #print(img)
    img_io = BytesIO()
    
    if isinstance(img, int):
        print('0')
    else:
        img.save(img_io, 'JPEG', quality=100)
        stream = img_io
        stream.seek(0)
        frame = stream.read()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def serve_pil_image(pil_img):
    print(pil_img)
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(return_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

def flaskServer():
    app.run(host="0.0.0.0", debug=False)

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


if __name__ == "__main__":
    global status

    thread5 = Thread(target=return_img)
    thread5.start()
    thread5.deamon = True

    thread = Thread(target=flaskServer)
    thread.start()
    sleep(2)
    signal.signal(signal.SIGINT, signal_handler)

