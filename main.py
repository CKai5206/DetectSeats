import caculateSeats
import glob
import os
import time as t
import xml.etree.ElementTree as ET
import targetObject
import connectDB
import cv2

def getCurrentTime():
    import re
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    today, time = now.split(" ")[0], now.split(" ")[1]
    time = re.sub(":",'', time)
    today = today.replace( today.split("-")[1], str(int(today.split("-")[1]) % 12))

    return today, time
def getImageFile(today, time):
    import cv2
    
    # imagePath = "..\\data\\140.134.174.233\\" + today + "\\sched"
    imagePath = "20190601125502000\\"
    files = glob.glob(os.path.join(imagePath,"*jpg"))
    
    return files

def readSeatsCoordinatesXml():
    
    tree = ET.parse("20190601125502000\\00001.xml")
    root = tree.getroot()
    seatsList = []
    for i in root.findall('object'):
        name = i.find("name").text
        lt_x = int(i.find("bndbox").find("xmin").text)
        lt_y = int(i.find("bndbox").find("ymin").text)
        rb_x = int(i.find("bndbox").find("xmax").text)
        rb_y = int(i.find("bndbox").find("ymax").text)
        seatsList.append(targetObject.seat(name, lt_x, lt_y, rb_x, rb_y))  
    connectDB.writeSeatsCoordinates("RenYanHall", seatsList)
def drawSeatsCoordinates(frame):
        seatsList = connectDB.getSeatsCoordinates("test2")
        for i in seatsList:
                lt_x = i.lt_x
                lt_y = i.lt_y
                rb_x = i.rb_x
                rb_y = i.rb_y
                cv2.rectangle(frame, (lt_x, lt_y), (rb_x, rb_y), (255,0,0))
        cv2.namedWindow("detectSeats", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('detectSeats', 1080,960)
        cv2.imshow("detectSeats", frame)
        cv2.waitKey(1)
        cv2.imwrite(os.getcwd()+"\\output\\image\\classSeats2.jpg",frame)
        cv2.destroyAllWindows()
def main():
        
        today, time = getCurrentTime()
        imagePath = getImageFile(today, time)
# #     readPeopleSeatsCoordinates()
        from caculateSeats import caculate
        from  detectPeople import processImage
        for i in imagePath:
                frame = processImage(i)
                drawSeatsCoordinates(frame)
        # caculate("RenYanHall")
    
        # info = [
        #         ("SeatCount", connectDB.getSeatsCounts('RenYanHall')),
        # ]
        # for index, (k, v) in enumerate(info):
        #         text = "{}: {}".format(k, v)
        #         cv2.putText(frame, text, ( 0 + (index * 30) + 250  , frame.shape[0] - (index * 20) - 30 ),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # cv2.namedWindow("detectSeats", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('detectSeats', 1080,960)
        # cv2.imshow("detectSeats", frame)
        # cv2.waitKey(0)
        # # cv2.imwrite(os.getcwd()+"\\output\\image\\classSeats2.jpg",frame)
        # cv2.destroyAllWindows()    

# while(True):
#     main()
main()