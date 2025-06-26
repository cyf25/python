from ultralytics import YOLO
import cv2

a1= YOLO('yolov8n.pt')

a1(source=r'basics\YOLO\Wastesorting\2.jpg',show=True, save=True)