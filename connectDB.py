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

def getSeatsCoordinates():
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("select name, lt_x, lt_y, rb_x, rb_y from class_room_seats")#下指令，皆用變數儲存
        
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

def writePeopleCoordinates(peopleCoordinates):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        for person in peopleCoordinates:
            sql = "INSERT INTO person_coordinates VALUES('%s',%d,%d,%d,%d)" \
                %(person['object'], person['lt_x'], person['lt_y'], person['rb_x'], person['rb_y'])#下指令，皆用變數儲存
            cursor.execute(sql)
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 


def writeSeatsCounts(seatsCounts):
    db = open_db()
    try:
        cursor = db.cursor()#建立資料庫游標
        sql = ("UPDATE seats_counts SET Vacancy =" +str(seatsCounts)+ " \
         WHERE location = 'classRoom1'" )#下指令，皆用變數儲存
        cursor.execute(sql)
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        db.close()#關閉DataBase 