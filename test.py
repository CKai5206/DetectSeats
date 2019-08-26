import cv2
import os
import numpy as np
import targetObject


a = targetObject.seat("seat", 3, 5, 7,2)
b = targetObject.person("person", 4 , 8, 9, 6)

print(intersects(a,b))