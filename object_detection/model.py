from ultralytics import YOLO
import sys

model = YOLO("yolov8n.pt")
dict_classes = model.model.names
print(dict_classes)

model.train(data='/home/stian/repos/CS569_project/object_detection/Data.yaml', epochs=50, batch=10)

results = model.predict(source='/home/stian/repos/CS569_project/object_detection/valid/images',save = True)
