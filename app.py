# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo which runs object classification and streams video to the browser.

export TEST_DATA=/usr/lib/python3/dist-packages/edgetpu/test_data

python3 -m edgetpuvision.classify_server \
  --model ${TEST_DATA}/mobilenet_v2_1.0_224_inat_bird_quant.tflite \
  --labels ${TEST_DATA}/inat_bird_labels.txt
"""
from edgetpuvision.apps2 import run_server
from edgetpuvision.classify import add_render_gen_args, render_gen
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

app = Flask(__name__)


l = run_server(add_render_gen_args, render_gen)



def return_img():
  while True:
        
    img = l.image()
    # print(img)
    img_io = BytesIO()

    if img == 0:
        print("0")
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

