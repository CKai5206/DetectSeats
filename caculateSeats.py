import connectDB

def checkOverlap(seat, person):
    return not(seat.lt_x > person.rb_x \
                or seat.rb_x < person.lt_x \
                or seat.lt_y > person.rb_y \
                or seat.rb_y < person.lt_y)


def caculateArea(seat, person):
    if checkOverlap(seat, person):
        dx = abs(min(seat.rb_x, person.rb_x) - max(seat.lt_x, person.lt_x))
        dy = abs(min(seat.lt_y, person.lt_y) - max(seat.rb_y, person.rb_y))
        seatArea = abs((seat.rb_x - seat.lt_x) * (seat.lt_y - seat.rb_y))
        
        if (dx * dy) / seatArea > 0.5:
                return True
        else:return False


def mergeCaculate():
    peopleCoordinates = connectDB.getPeopleCoordinates()
    seatsCoordinates = connectDB.getSeatsCoordinates("class_room_seats")
    count = 0
    
    for seat in seatsCoordinates:
        for person in peopleCoordinates:
            if person.sit is not True:
                result = caculateArea(seat, person)
                if result:
                    person.sit = True
                    count += 1
                    break
    return count

def caculate(location):
        seatsCount = mergeCaculate()
        lastSeats = connectDB.getOldSeatsCounts()
        # print("seatsCount", seatsCount, "lastCount", lastSeats)
        connectDB.writeSeatsCounts(lastSeats, "lastSeats",location)
        connectDB.writeSeatsCounts(seatsCount,"NowSeats",location)