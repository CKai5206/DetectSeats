# import detectPeople.processImage
import caculateSeats
import glob
import os
import time as t
import xml.etree.ElementTree as ET
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
    
    files = glob.glob(os.path.join(imagePath,"*jpg"))
    return files[-1]

def readPeopleCoordinates():
    
    tree = ET.parse("..\\20190601125502000\\00001.xml")
    root = tree.getroot()
    
    for i in root.findall('object'):
        print(i.find("name").text)
        lt_x =i.find("bndbox").find("xmin").text
        lt_y = i.find("bndbox").find("ymin").text
        rb_x = i.find("bndbox").find("xmax").text
        rb_y = i.find("bndbox").find("ymax").text
def main():
    # today, time = getCurrentTime()
    # imagePath = getImageFile(today, time)

    # from  detectPeople import processImage
    # processImage(imagePath)
    
    # from caculateSeats import caculate
    # caculate()
    # print("caculating")
    readPeopleCoordinates()

# while(True):
#     main()
main()