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

import argparse
import logging

import threading
import signal
from . import gstreamer
from . import pipelines
# from .camera import make_camera
from .gstreamer import Display
# from .streaming.server import StreamingServer
from .gst import *
from PIL import Image

from . import svg

EMPTY_SVG = str(svg.Svg())

class NAL:
    CODED_SLICE_NON_IDR = 1  # Coded slice of a non-IDR picture
    CODED_SLICE_IDR     = 5  # Coded slice of an IDR picture
    SEI                 = 6  # Supplemental enhancement information (SEI)
    SPS                 = 7  # Sequence parameter set
    PPS                 = 8  # Picture parameter set


ALLOWED_NALS = {NAL.CODED_SLICE_NON_IDR,
                NAL.CODED_SLICE_IDR,
                NAL.SPS,
                NAL.PPS,
                NAL.SEI}


class run_server():
    def __init__(self, add_render_gen_args, render_gen):
        logging.basicConfig(level=logging.INFO)

        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--source',
                            help='/dev/videoN:FMT:WxH:N/D or .mp4 file or image file',
                            default='/dev/video0:YUY2:640x480:30/1')
        parser.add_argument('--bitrate', type=int, default=1000000,
                            help='Video streaming bitrate (bit/s)')
        parser.add_argument('--loop', default=False, action='store_true',
                            help='Loop input video file')

        add_render_gen_args(parser)
        self.args = parser.parse_args()

        self.gen = render_gen(self.args)
        self.camera = self.make_camera(self.args.source, next(self.gen), self.args.loop)
        self._camera = self.camera
        assert self.camera is not None
        self.overlay = 0
        self.img = 0
        self._bitrate=1000000
        self._start_recording()
    
    def make_camera(self, source, inference_size, loop):
        fmt = parse_format(source)
        if fmt:
            return DeviceCamera(fmt, inference_size)

        filename = os.path.expanduser(source)
        if os.path.isfile(filename):
            return FileCamera(filename, inference_size, loop)

        return None


    def _start_recording(self):
        
        self._camera.start_recording(self, format='h264', profile='baseline',
            inline_headers=True, bitrate=self._bitrate, intra_period=0)

    def _stop_recording(self):
        
        self._camera.stop_recording()

    def return_frame(self):

        self._camera.request_key_frame()
    def image(self):
            
            
        

        self.camera.render_overlay = self.render_overlay
        return(self.img)
        # signal.pause()
    

    def render_overlay(self, tensor, layout, command):
            test = tensor.reshape(224, 224, 3)
            im = Image.fromarray(test)
            # im.save("eee.jpeg")
            
            self.img = im
            
            self.overlay = self.gen.send((tensor, layout, command))

    def write(self, data):
        """Called by camera thread for each compressed frame."""
        assert data[0:4] == b'\x00\x00\x00\x01'
        frame_type = data[4] & 0b00011111
        
            




class Camera:
    def __init__(self, render_size, inference_size, loop):
        self._layout = gstreamer.make_layout(inference_size, render_size)
        self._loop = loop
        self._thread = None
        self.render_overlay = None

    @property
    def resolution(self):
        return self._layout.render_size


    def start_recording(self, obj, format, profile, inline_headers, bitrate, intra_period):
       
        def on_buffer(data, _):
            

            
            pass

        def render_overlay(tensor, layout, command):
            
            if self.render_overlay:
                self.render_overlay(tensor, layout, command)
            return None

        signals = {
          'h264sink': {'new-sample': gstreamer.new_sample_callback(on_buffer)},
        }
       
        hello = gstreamer.new_sample_callback(on_buffer)
        print(hello)
        pipeline = self.make_pipeline(format, profile, inline_headers, bitrate, intra_period)

        self._thread = threading.Thread(target=gstreamer.run_pipeline,
                                        args=(pipeline, self._layout, self._loop,
                                              render_overlay, gstreamer.Display.NONE,
                                              False, signals))
        self._thread.start()

    def stop_recording(self):
        gstreamer.quit()
        self._thread.join()

    def make_pipeline(self, fmt, profile, inline_headers, bitrate, intra_period):
        raise NotImplemented

class FileCamera(Camera):
    def __init__(self, filename, inference_size, loop):
        info = gstreamer.get_video_info(filename)
        super().__init__((info.get_width(), info.get_height()), inference_size,
                          loop=loop)
        self._filename = filename

    def make_pipeline(self, fmt, profile, inline_headers, bitrate, intra_period):
        return pipelines.video_streaming_pipeline(self._filename, self._layout)

class DeviceCamera(Camera):
    def __init__(self, fmt, inference_size):
        super().__init__(fmt.size, inference_size, loop=False)
        self._fmt = fmt

    def make_pipeline(self, fmt, profile, inline_headers, bitrate, intra_period):
        return pipelines.camera_streaming_pipeline(self._fmt, profile, bitrate, self._layout)

            


def run_app(add_render_gen_args, render_gen):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--source',
                        help='/dev/videoN:FMT:WxH:N/D or .mp4 file or image file',
                        default='/dev/video0:YUY2:1280x720:30/1')
    parser.add_argument('--loop',  default=False, action='store_true',
                        help='Loop input video file')
    parser.add_argument('--displaymode', type=Display, choices=Display, default=Display.FULLSCREEN,
                        help='Display mode')
    add_render_gen_args(parser)
    args = parser.parse_args()

    if not run_gen(render_gen(args),
                   source=args.source,
                   loop=args.loop,
                   display=args.displaymode):
        print('Invalid source argument:', args.source)
class NAL:
    CODED_SLICE_NON_IDR = 1  # Coded slice of a non-IDR picture
    CODED_SLICE_IDR     = 5  # Coded slice of an IDR picture
    SEI                 = 6  # Supplemental enhancement information (SEI)
    SPS                 = 7  # Sequence parameter set
    PPS                 = 8  # Picture parameter set

