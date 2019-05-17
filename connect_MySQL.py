import mysql.connector
from 

def connect():
    """ Connect to MySQL database """

    try:
        password = input("What is your password to connect to EG Cleaning?\n")
        conn = mysql.connector.connect(host='50.87.144.133',
                                       database='egcleani_EG_Cleaning',
                                       user='egcleani_erik',
                                       password=password)
        
        if conn.is_connected():
            print('Connected to MySQL database')
            cur=conn.cursor() 

    except mysql.connector.Error as error : 
        conn.rollback()
        print("Failed to insert into MySQL table {}".format(error))
  
    finally:
        cur.close()
        conn.close()
        print("MySQL connection is closed")
  
if __name__ == '__main__':
    connect()
    print("End of Program")