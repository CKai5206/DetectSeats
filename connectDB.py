import pymysql
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
        return rows
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
        return rows
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


def writeSeatsCounts():
    pass
    db = open_db()