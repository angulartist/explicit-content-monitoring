import logging
import os

import apache_beam as beam
import cv2

from ml_processing.deeper import Deeper

SAVED_ML_DIR = 'trained'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EXPORTED_DIR = os.path.join(DIR_PATH, SAVED_ML_DIR)

SAVED_MODEL_PATH = os.path.join(EXPORTED_DIR, 'frozen_inference_graph.pb')
SAVED_PROTO_PATH = os.path.join(EXPORTED_DIR, 'model.pbtxt')


class DetectLabelsFn(beam.DoFn):

    def __init__(self):
        self.model = None

    def setup(self):
        logging.info("[ML] Loading the model 🥶")
        net = cv2.dnn.readNetFromTensorflow(SAVED_MODEL_PATH, SAVED_PROTO_PATH)
        self.model = Deeper(net, confidence=.3)

    def process(self, element):
        self.model.detect(element)

        yield self.model.detect(element)