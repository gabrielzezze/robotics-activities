# Para RODAR
# python atividade3_item2_3.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# Credits: https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/

print("Para executar:\npython atividade3_item2_3.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel")

# import the necessary packages
import numpy as np
import argparse
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time

(major, minor) = cv2.__version__.split(".")[:2]

if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args["tracker"].upper())

else:
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }
    tracker = OPENCV_OBJECT_TRACKERS["csrt"]()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# (note: normalization is done via the authors of the MobileNet SSD
# implementation)


garrafa = 0

def detect(frame):
    global garrafa
    global x_person
    global y_person
    global l_person
    global h_person
    image = frame.copy()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    results = []

    for i in np.arange(0, detections.shape[2]):

        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the `detections`, then compute the (x, y)-coordinates of the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction            

            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY), (endX, endY),COLORS[idx], 2)

            y = startY - 15 if startY - 15 > 15 else startY + 15

            cv2.putText(image, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            results.append((CLASSES[idx], confidence*100, (startX, startY),(endX, endY) ))

            if CLASSES[idx] == 'bottle':  
                x_person = startX
                y_person = startY
                l_person = endX - startX
                h_person = endY - startY
                print(l_person)
                print(h_person)
                garrafa+=1

    return image, results

#cap = cv2.VideoCapture('hall_box_battery_1024.mp4')
cap = cv2.VideoCapture(0)

print("Known classes")
print(CLASSES)

while(True):
    print("Contador: {}".format(garrafa))
    passa = True
    if garrafa<5:

        ret, frame = cap.read()
        
        frame = imutils.resize(frame,width=400)

        result_frame, result_tuples = detect(frame)
        cv2.imshow('Frame',result_frame)


    else:
        ret, frame = cap.read()

        if passa:
            initBB = (x_person,y_person,l_person,h_person)
            tracker.init(frame, initBB)
            passa = False

        frame = imutils.resize(frame, width=400)
        (H, W) = frame.shape[:2]
        try:
            (success, box) = tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 0, 255), 2)            
            #else:
            #    garrafa = 0
        except:
            #pass
            garrafa = 0      
        
        cv2.imshow('Frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
