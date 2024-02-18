
import ultralytics
from ultralytics import YOLO
from roboflow import Roboflow
import os
import logging
import torch
torch.cuda.is_available()
torch.cuda.device_count()
os.environ['CUDA_VISIBLE_DEVICES']

from roboflow import Roboflow
rf = Roboflow(api_key="H71fcsU56T78bycY0nPK")
project = rf.workspace("gaurang-ingle-qqgvw").project("person-d4oe4")
dataset = project.version(1).download("yolov8")


device = 'cuda' if torch.cuda.is_available() else 'cpu'
batch=2
task = 'detect'
mod = 'YOLOv8n.pt'
dataset_directory = r"C:/Users/gaura/Desktop/iPython/Personal Projects/Auto Object Detection/person--1/data.yaml"
epoch = 5
imgsz = 32
cache = 'disk'
# command = f"yolo task={task} mode=train model={mod} data={dataset_directory} epochs={epoch} imgsz={imgsz} cache={cache}"
# YOLO(mod)(task=task, mode='train', model=mod, data=dataset_directory, epochs=epoch, imgsz=imgsz, cache=cache)
# Load a model
model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights


results = model.train(task=task, data=dataset_directory, epochs=epoch, imgsz=imgsz, batch=batch, cache=cache, device = device)

g = help(YOLO)




# Train the model
results = model.train(data=dataset_directory, epochs=1, imgsz=640)




# Execute the YOLO command
import subprocess
subprocess.run(command, shell=True)
print("Training started...")