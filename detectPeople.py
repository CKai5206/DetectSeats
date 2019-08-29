import os
import cv2
import argparse
import sys
import numpy as np
import pandas as pd
import csv
import connectDB

# Initialize the parameters
confThreshold = 0.6  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image
        
# Load names of classes
classesFile = "coco.names";
# classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3.cfg";
modelWeights = "yolov3.weights";

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

# initialize the frame dimensions (we'll set them as soon as we read
# the first frame from the video)
(W, H) = (None, None)

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def processOutPuts(frame, outputs):
    (countPerson, countChair) = (0, 0)
    (classIDs, confidences, boxes, targetCoordinates) = ([], [], [], [])
    (H, W) = frame.shape[:2]
    # Output為Model三層Net的個別輸出
    for output in outputs:
        # 在每層輸出中的[5:]為每個物品預測的相關值結果，採用One-Hot-Encoding格式
        for detection in output:
            scores = detection[5:]
            # np.argmax用來找出最高score的index
            classID = np.argmax(scores)
            # confidence為最高的score的值
            confidence = scores[classID]
            # confThreshold為準確度標準，要超過0.6才判斷為成功預測
            if confidence > confThreshold:
                # detection[:2]為預測出來目標的中心 (x,y) 座標，
                # detection[3:4]為預測出來目標的寬跟高的長度，
                # 要再乘上原圖的比例來決定在整張圖的座標、比例
                box = detection[:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                left = int(centerX - width / 2)
                top = int(centerY - height / 2)
                
                boxes.append([left, top, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        if classIDs[i] == 0:
            countPerson += 1
            drawPred(frame, classIDs[i], confidences[i], left, top, left + width, top + height, (0, 0, 255))
            
            targetCoordinates.append({
                "object":"Person",
                "lt_x":left,
                "lt_y":top,
                "rb_x":left + width,
                "rb_y":top + height
            })
        
    info = [
        ("Person", countPerson)
    ]

    # loop over the info tuples and draw them on our frame
    for index, (k, v) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv2.putText(frame, text, ( 10, frame.shape[0] - (index * 20) - 30 ),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return targetCoordinates


def drawPred(frame, classID, conf, left, top, right, bottom, RGB):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), RGB)
    # Get the label for the class name and its confidence
    label = classes[classID] + ":" + "%.1f" % (conf * 100) + "%"
    #Display the label at the top of the bounding box
    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_DUPLEX, 0.6, RGB, 1)

def processImage(framePath):
    # print(os.getcwd() + framePath)
    frame = cv2.imread(os.getcwd() + "\\"+framePath)
    frameName = framePath.split("\\")[-1]
    
    # 將通過 blobFromImage 函數將其轉換爲神經網絡的輸入blob。
    # 在此過程中，它使用比例因子1/255 將圖像像素值縮放到0到1的目標範圍。
    # 它還將圖像的大小縮放爲給定的大小（416,416）而不進行裁剪。
    # 請注意，我們不在此處執行任何均值減法，因此將[0,0,0]傳遞給函數的mean參數，
    # 並將swapRB參數保持爲其默認值1
    blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0, 0, 0], swapRB = 1, crop=False)

    net.setInput(blob)

    outputs = net.forward(getOutputsNames(net))
    peopleCoordinates = processOutPuts(frame, outputs)
    
    # cv2.imshow("Person detection", frame)
    # cv2.waitKey(50)
    # cv2.destroyAllWindows()
    import connectDB
    connectDB.writePeopleCoordinates(2,peopleCoordinates)
    
    return frame
    


def processVideo(videoPath):
    cap = cv2.VideoCapture(os.getcwd() + videoPath)
    from caculateSeats import caculate
    outputFile = "outputVideo.mp4"
    vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
    while cap.isOpened():
        # get frame from the video
        hasFrame, frame = cap.read()
        if hasFrame:
            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
            # Sets the input to the network
            net.setInput(blob)
            # Runs the forward pass to get output of the output layers
            outputs = net.forward(getOutputsNames(net))
            # Remove the bounding boxes with low confidence
            personCoordinates = processOutPuts(frame, outputs)
            connectDB.writePeopleCoordinates(2,personCoordinates)

            caculate("RenYanHall")

            seatsList = connectDB.getSeatsCoordinates("test2")
            for i in seatsList:
                drawPred(frame, 57, 0.0, i.lt_x, i.lt_y, i.rb_x, i.rb_y, (0,255,0))
            info = [
                ("SeatCount", connectDB.getSeatsCounts('RenYanHall')),
            ]
            for index, (k, v) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, ( 0 + (index * 30) + 250  , frame.shape[0] - (index * 20) - 30 ),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.resizeWindow('detectSeats', 1080,960)
            cv2.namedWindow("detectSeats", cv2.WINDOW_NORMAL)
            cv2.imshow("Person detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            vid_writer.write(frame.astype(np.uint8))
        elif not hasFrame:
            print("Done processing !!!")
            cv2.waitKey(3000)
            cap.release()
            cv2.destroyAllWindows()
            break

# processVideo(videoPath = "\\media\\video\\class01.mp4")