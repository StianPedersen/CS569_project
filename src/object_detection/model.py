from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import yaml

import pandas as pd
import numpy as np

model = YOLO("yolov8n.pt")
dict_classes = model.model.names
print(dict_classes)

model.train(data='/home/stian/repos/CS569_project/src/object_detection/Data.yaml', epochs=50, batch=8)

results = model.predict(source='/home/stian/repos/CS569_project/src/object_detection/valid/images',save = True)
