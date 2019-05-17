import mysql.connector

password = input("What is your password to connect to EG Cleaning?\n")
conn = mysql.connector.connect(host='50.87.144.133',
                                database='egcleani_EG_Cleaning',
                                user='egcleani_erik',
                                password=password)
cur=conn.cursor() 
#Get EMPLOYEE ID by his/her name
def getEmpId():
    emp = input("Search for employee: \n")
    cur.execute("SELECT EmpId FROM Employee WHERE (EmpFirstNam IN ('%s') OR EmpLastNam IN ('%s'))" % (emp, emp))
    empId = cur.fetchone()
    empId = empId[0]             
    return empId

#Get employee email
def getEmpEmail():
    emp = getEmpId()

    select_query = ("SELECT empEmail FROM Employee WHERE EmpId = %s" % emp)
    cur.execute(select_query)
    email = cur.fetchone()
    email = email[0]
    return email

email = getEmpEmail()
print(email)