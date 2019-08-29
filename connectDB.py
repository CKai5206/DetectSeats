import pymysql
import targetObject
def open_db():#開啟Database
    import pymysql.cursors
    db = pymysql.connect(host='140.134.26.4',#連結MySQL
                        user='public_root',
                        password='*gis5200',                             
                        db='human',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    return db

def getPeopleCoordinates():
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("select * from person_coordinates")#下指令，皆用變數儲存
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        people = []

        for line in rows:
            person = targetObject.person('person', line['lt_x'], line['lt_y'], line['rb_x'], line['rb_y'], False)
            people.append(person)
        return people

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 

def getSeatsCoordinates(location):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("select name, lt_x, lt_y, rb_x, rb_y from " + str(location))#下指令，皆用變數儲存
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        seats = []

        for line in rows:
            seat = targetObject.seat(line['name'], line['lt_x'], line['lt_y'], line['rb_x'], line['rb_y'])
            seats.append(seat)
        return seats 

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 

def writePeopleCoordinates(roomId, peopleCoordinates):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = "DELETE FROM person_coordinates"
        cursor.execute(sql)
        
        for person in peopleCoordinates:    
            sql = "INSERT INTO person_coordinates VALUES(%d, '%s', %d, %d, %d, %d)" \
                %(roomId, person['object'], person['lt_x'], person['lt_y'], person['rb_x'], person['rb_y'])#下指令，皆用變數儲存
            cursor.execute(sql)
        
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 

def writeSeatsCoordinates(roomName, seatsList):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("select id from class_room where name Like ('%s') " %roomName)
        cursor.execute(sql)
        roomID = cursor.fetchone()
        for seat in seatsList:
            print(seatsList.index(seat) + 57 ,roomID['id'], "0-0", "S" + str(seatsList.index(seat) + 1), seat.lt_x, seat.lt_y, seat.rb_x, seat.rb_y, "")   
            sql = "INSERT INTO test2 VALUES(%d, %d, '%s','%s', %d, %d, %d, %d, '%s')" \
                %(seatsList.index(seat) + 57 ,roomID['id'], "0-0", "S" + str(seatsList.index(seat) + 1), seat.lt_x, seat.lt_y, seat.rb_x, seat.rb_y, "")#下指令，皆用變數儲存
            cursor.execute(sql)
            print(1)
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 

def getOldSeatsCounts():
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        
        sql = ("select NowSeats from seats_counts" )#下指令，皆用變數儲存
        cursor.execute(sql)
        oldSeatsCount = cursor.fetchall()
        
        return oldSeatsCount[0]['NowSeats']
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 



def writeSeatsCounts(seatsCounts, category, location):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("UPDATE seats_counts SET " +category+ " =" +str(seatsCounts)+ " \
         WHERE location = ('%s')" %location )#下指令，皆用變數儲存
        cursor.execute(sql)
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 

def getSeatsCounts(locatoin):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("select allSit,lastSeats from seats_counts where location Like ('%s') " %(locatoin) )#下指令，皆用變數儲存
        cursor.execute(sql)
        seatsCount = cursor.fetchall()
        return seatsCount[0]['allSit'] - seatsCount[0]['lastSeats']
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 

