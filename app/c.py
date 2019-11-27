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

"""A demo which runs object classification on camera frames.

export TEST_DATA=/usr/lib/python3/dist-packages/edgetpu/test_data

python3 -m edgetpuvision.classify \
  --model ${TEST_DATA}/mobilenet_v2_1.0_224_inat_bird_quant.tflite \
  --labels ${TEST_DATA}/inat_bird_labels.txt
"""
import argparse
import collections
import itertools
import time

from edgetpu.classification.engine import ClassificationEngine

from . import utils
from .apps import run_app



def top_results(window, top_k):
    total_scores = collections.defaultdict(lambda: 0.0)
    for results in window:
        for label, score in results:
            total_scores[label] += score
    return sorted(total_scores.items(), key=lambda kv: kv[1], reverse=True)[:top_k]

def accumulator(size, top_k):
    window = collections.deque(maxlen=size)
    window.append((yield []))
    while True:
        window.append((yield top_results(window, top_k)))

def print_results(inference_rate, results):
    print('\nInference (rate=%.2f fps):' % inference_rate)
    print(results)
    for label, score in results:
        print('  %s, score=%.2f' % (label, score))


def add_render_gen_args(parser):
    default_model_dir = "./app/all_models"
    default_model = 'mobilenet_v2_1.0_224_quant_edgetpu.tflite'
    #default_model = 'model_edgetpu.tflite'
    default_labels = 'imagenet_labels.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                            default=default_model)
    parser.add_argument('--labels', help='label file path',
                            default=default_labels)
    parser.add_argument('--window', type=int, default=10,
                        help='number of frames to accumulate inference results')
    parser.add_argument('--top_k', type=int, default=3,
                        help='number of classes with highest score to display')
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='class score threshold')
    parser.add_argument('--print', default=False, action='store_true',
                        help='Print inference results')

def main():
    run_app(add_render_gen_args, render_gen)



class Model():
    def __init__(self):
        
        # self.engine = ClassificationEngine(os.path.join(default_model_dir, self.args.model))
        # self.labels = load_labels(os.path.join(default_model_dir, self.args.labels))


        # self.last_time = time.monotonic()

    def user_callback(self,image):
        acc = accumulator(size=args.window, top_k=args.top_k)
        acc.send(None)  # Initialize.

        fps_counter = utils.avg_fps_counter(30)

        engines, titles = utils.make_engines(args.model, ClassificationEngine)
        assert utils.same_input_image_sizes(engines)
        engines = itertools.cycle(engines)
        engine = next(engines)

        labels = utils.load_labels(args.labels)
        draw_overlay = True

        yield utils.input_image_size(engine)

        output = None
        
        tensor, layout, command = (yield output)

        inference_rate = next(fps_counter)
        if draw_overlay:
            start = time.monotonic()
            results = engine.classify_with_input_tensor(tensor, threshold=args.threshold, top_k=args.top_k)
            inference_time = time.monotonic() - start

            results = [(labels[i], score) for i, score in results]
            results = acc.send(results)
            if args.print:
                print_results(inference_rate, results)

            title = titles[engine]
            output = overlay(title, results, inference_time, inference_rate, layout)
        else:
            output = None

    

model = None
def main():
    global model
    model = Model()
class AI():
  def __init__(self):
    self.type = "objClass"
    main()
  def run(self, img):
    if (img != None):
      return(model.user_callback(img))