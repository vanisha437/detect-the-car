import numpy as np
import cv2


confidenceThreshold = 0.1
NMSThreshold = 0.1

modelConfiguration = 'cfg/yolov3.cfg'
modelWeights = 'yolov3.weights'

labelsPath = 'coco.names'

labels = open(labelsPath).read().strip().split('\n')

yoloNetwork = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

# Read the input video file instead of an image
image = cv2.imread("car.png")
video = cv2.VideoCapture("car.mp4")
# Define infinite while loop
while True:
# Read the first frame of the video which returns two value check, image
    check, image = video.read()

#Run the code only if the video frame is read successfully i.e value of check is True
if check:
    if labels[classIds[i]] == "car":

image = cv2.resize(image, (0, 0), fx=1, fy=1)
dimensions = image.shape[:2]
H, W = dimensions

blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416))
yoloNetwork.setInput(blob)

layerName = yoloNetwork.getUnconnectedOutLayersNames()
layerOutputs = yoloNetwork.forward(layerName)

boxes = []
confidences = []
classIds = []

for output in layerOutputs:
    for detection in output:
        scores = detection[5:]
        classId = np.argmax(scores)
        confidence = scores[classId]

        if confidence > confidenceThreshold:
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY,  width, height) = box.astype('int')
            x = int(centerX - (width/2))
            y = int(centerY - (height/2))

            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIds.append(classId)

indexes = cv2.dnn.NMSBoxes(
    boxes, confidences, confidenceThreshold, NMSThreshold)

for i in range(len(boxes)):
    if i in indexes:
        # Write condition to detect the car in the image

        x, y, w, h = boxes[i]
        color = (255, 0, 0)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)


cv2.imshow('Moving Car', image)
# Change waitKey to 1
cv2.waitKey(1)

# Quit the display window when the spacebar key is pressed
key = cv2.waitKey(1)