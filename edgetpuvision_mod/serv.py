import queue
import threading
import requests
from apps import run_server
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
import keyboard 

import queue

from detect import add_render_gen_args, render_gen
from classify import add_render_gen_args1, render_gen1
# app = Flask(__name__)




# class DataStore():
#     a = None
#     c = None


# data = DataStore()
val = input()
print(val)
if val == '1':
    

    run_server(add_render_gen_args, render_gen)
else:
    print("here")
    run_server(add_render_gen_args1, render_gen1)





# import sys, termios, tty, os, time
 
# def getch():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
 
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch
 
# button_delay = 0.2
 
# while True:
#     char = getch()
 
#     if (char == "p"):
#         print("Stop!")
#         exit(0)
 
#     if (char == "a"):
#         print("Left pressed")
#         thread.join()
#         time.sleep(button_delay)
 
#     elif (char == "d"):
#         print("Right pressed")
#         time.sleep(button_delay)
 




# @app.route('/video_feed')
# def video_feed():
#     a = run_server(add_render_gen_args, render_gen)
    
#     data.a = a
#     return 'Video 1'

# @app.route('/video_feed1')
# def video_feed1():
    
#     data.a.__exit__()
#     run_server(add_render_gen_args1, render_gen1)
#     return 'Video 2'


# @app.route('/')
# def index():
#     return render_template('index.html')



# def flaskServer():
#     app.run(host="0.0.0.0", debug=False)

# def signal_handler(signal, frame):
#     print("\nprogram exiting gracefully")
#     sys.exit(0)


# if __name__ == "__main__":
    
        

#     thread = Thread(target=flaskServer)
#     thread.start()
#     sleep(2)
#     signal.signal(signal.SIGINT, signal_handler)



