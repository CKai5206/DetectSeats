from collections import namedtuple
import connectDB
import matplotlib.pyplot as plt
import numpy as np

def checkOverlap(seat, person):
    return not(seat.lt_x > person.rb_x
        or seat.rb_x < person.lt_x
        or seat.lt_y < person.rb_y
        or seat.rb_y > person.lt_y)

def caculateArea(seat, person):
    if checkOverlap(seat, person):
        dx = abs(min(seat.rb_x, person.rb_x) - max(seat.lt_x, person.lt_x))
        dy = abs(min(seat.lt_y, person.lt_y) - max(seat.rb_y, person.rb_y))
        seatArea = (seat.rb_x - seat.lt_x) * (seat.lt_y * seat.rb_y)
        print((dx * dy) / seatArea)


def caculate():
    peopleCoordinates = connectDB.getPeopleCoordinates()
    seatsCoordinates = connectDB.getSeatsCoordinates()
    count = 0
    for seat in seatsCoordinates:
        for person in peopleCoordinates:
            if person.sit is not True:
                result = caculateArea(seat, person)
                if result: 
                    person.sit = True
                    count += 1
                print(result)
#     Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
#     ra = Rectangle(3., 3., 5., 5.)
#     rb = Rectangle(1., 1., 4., 3.5)
#     # intersection here is (3, 3, 4, 3.5), or an area of 1*.5=.5

#     def area(a, b):  # returns None if rectangles don't intersect
#         dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
#         dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
#         if (dx>=0) and (dy>=0):
#             return dx*dy
#     print(area(ra, rb))
#     connectDB.writeSeatsCounts()
    


    

caculate()