import mysql.connector
from datetime import datetime

def connect():
    """ Connect to MySQL database """
    #password = input("What is your password to connect to EG Cleaning?\n")
    conn = mysql.connector.connect(host='50.87.144.133',
                                    database='egcleani_EG_Cleaning',
                                    user='egcleani_erik',
                                    password="Erik0408")
         
    if conn.is_connected():
        return conn
    else:
        return 0

def connectCursor():
    print('Connected to MySQL database')
    cur=connect()
    return cur