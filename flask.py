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
import threading
def t():
    run_server(add_render_gen_args, render_gen)


thread = threading.Thread(target=t)
thread.daemon = True                         
thread.start()  

def main():
  while True:
    print(' ')
if __name__ == '__main__':
    main()



# from app import Detect, Classify, Teachable, Empty, pose_camera, anonymizer, synthesizer
# from flask import Flask, send_file, Response, render_template
# from app.Cam import camera
# import keyboard
# from time import sleep
# from threading import Thread, active_count
# import signal
# from threading import Thread, Event
# from threading import Thread
# import sys

# app = Flask(__name__)

# Image = camera(Detect.AI())



# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(Image.ImageStream(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def flaskServer():
#     app.run(host="0.0.0.0", debug=False)

# def signal_handler(signal, frame):
#     print("\nprogram exiting gracefully")
#     sys.exit(0)

# def my_function():
#     while True:
#         sleep(0.01)
#         count = Image.numImages
#         fps = Image.fps
#         Inference = Image.inference
#         Class = Image.Class
#         Score = Image.Score


# if __name__ == "__main__":
#     global status
#     thread = Thread(target=flaskServer)
#     thread.start()
#     thread5 = Thread(target=my_function)
#     thread5.start()
#     sleep(2)
#     signal.signal(signal.SIGINT, signal_handler)

