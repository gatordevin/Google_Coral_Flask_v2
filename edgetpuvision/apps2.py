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
import signal

from .camera import make_camera
from .gstreamer import Display, run_gen
from .streaming.server import StreamingServer

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


# class test():
#     def __init__():
#         pass
#     def hello_function():
#         print('Hello World, it\'s me.  Function.')
#         return ("hello")

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
        self.camera = make_camera(self.args.source, next(self.gen), self.args.loop)
        self._camera = self.camera
        assert self.camera is not None
        self.overlay = 0
        self._bitrate=1000000
        self._start_recording()

    def _start_recording(self):
        
        self._camera.start_recording(self, format='h264', profile='baseline',
            inline_headers=True, bitrate=self._bitrate, intra_period=0)

    def _stop_recording(self):
        
        self._camera.stop_recording()

    def return_frame(self):

        self._camera.request_key_frame()
    def image(self):
        
        # test = self.return_frame()
        # print(test)
        # with StreamingServer(self.camera, self.args.bitrate) as server:
        def render_overlay(tensor, layout, command):
            test = tensor.reshape(224, 224, 3)
            im = Image.fromarray(test)
            im.save("your_file.jpeg")
            
            overlay = self.gen.send((tensor, layout, command))
            print(overlay)
            self.overlay = overlay

        self.camera.render_overlay = render_overlay
        signal.pause()

    def write(self, data):
        """Called by camera thread for each compressed frame."""
        assert data[0:4] == b'\x00\x00\x00\x01'
        frame_type = data[4] & 0b00011111
        if frame_type in ALLOWED_NALS:
            self._camera.request_key_frame()
        
        
            


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