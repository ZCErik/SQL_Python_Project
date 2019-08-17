import mysql.connector

conn = mysql.connector.connect(host='50.87.144.133',
                                database='egcleani_EG_Cleaning',
                                user='egcleani_erik',
                                password="Erik0408")

cur=conn.cursor()
#Get EMPLOYEE ID by his/her name
def getEmpId():
    emp = input("Search for employee: \n")
    cur.execute("SELECT EmpId FROM Employee WHERE (EmpFirstNam LIKE ('%%%s%%') OR EmpLastNam LIKE ('%%%s%%'))" % (emp, emp))
    empId = cur.fetchone()
    empId = empId[0]             
    return empId

#Get employee email
def getEmpEmail(emp):
    select_query = ("SELECT empEmail FROM Employee WHERE EmpId = %s" % emp)
    cur.execute(select_query)
    email = cur.fetchone()
    email = email[0]
    return email

#Get employee first name
def getEmpName(emp):
    select_query = ("SELECT empFirstNam FROM Employee WHERE EmpId = %s" % emp)
    cur.execute(select_query)
    name = cur.fetchone()
    name = name[0]
    return name