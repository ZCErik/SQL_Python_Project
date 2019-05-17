import sys
sys.path.append('C:\\Users\\Erik Gabril\\Desktop\\MySQL_Python\\SQL_Python_Project\\eg_cleaning.py')

from datetime import datetime
from connect_MySQL import connect

#Register Customer
def registerCustomer():
    firstName = input("First Name: ")
    cur.execute("SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'egcleani_EG_Cleaning' AND TABLE_NAME = 'Customer'")
    custId = cur.fetchone()
    custId = custId[0]
    print(custId)
    lastName = input("Last Name: ")
    street = input("Street address: ")
    phone = input("Phone Number: ")
    postalCode = insertPostal()
    email = input("Email: ")
    note = input("Notes: ")
    ref = input("Referral: ")
    
    records_to_insert = (custId, firstName, lastName, street, phone, postalCode, email, note, ref)
    
    sql_insert_customer = """ INSERT INTO Customer (`custId`, `CustFirstNam`, `CustLastNam`, `custStreet`, `custPhone`, `custPostalCode`, `custEmail`, `Notes`, `referral`)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    
    cur.execute(sql_insert_customer, records_to_insert)
    conn.commit()

#Get customer ID by his/her name (first or last)  
#Validate if more than one customer with same name is found
def getCustId():
    name = input("Search for customer: \n")
    cur.execute("SELECT custId FROM Customer WHERE (CustFirstNam IN ('%s') OR CustLastNam IN ('%s'))" % (name, name))
    customers = cur.fetchall()
    customers = [ i[0] for i in customers ] #Clear ID numbers

    #If more than 1 customer with same name, show all to user pick                    
    if len(customers) > 1:
        i = 1
        print("Which", name, "would you like to choose?")
        for row in customers:
            cur.execute("SELECT CustFirstNam, CustLastNam FROM Customer WHERE custId = '%s'" % row)
            print(i, " - ", cur.fetchone())
            i += 1
        
        
        #Loop to pick only valid data
        option = input("Enter a valid option: \n")
        customer = customers[int(option)-1]

        cur.execute("SELECT CustFirstNam, CustLastNam FROM Customer WHERE custId = '%s'" % customer)
        cust = cur.fetchone()
        cust = cust[0] + " " +cust[1]
        
        return customers[customer]
    
    else:
        return customers[0]

#Insert POSTAL CODE
def insertPostal():
    zipCode = input("Please enter Postal Code: Eg. A1B 2C3\n")
    city = input("Please enter the City: \n")
    region = input("Please enter the Region: \n")
    
    recordsToInsert = (zipCode, city, region)
    sql_insert_postal = ("INSERT INTO `ZipCode` (`PostalCode`, `PostalCity`, `PostalRegion`) VALUES (%s, %s, %s)")
    
    cur.execute(sql_insert_postal, recordsToInsert)
    conn.commit
    return zipCode
    
#Get EMPLOYEE ID by his/her name
def getEmpId():
    emp = input("Search for employee: \n")
    cur.execute("SELECT EmpId FROM Employee WHERE (EmpFirstNam IN ('%s') OR EmpLastNam IN ('%s'))" % (emp, emp))
    empId = cur.fetchone()
    empId = empId[0]             
    return empId

#Function to insert Services into Invoices   
def insertServiceInvoices(InvoiceId, lineNo, ServId, EmpId, ServiceDate, HourlyOfService, Notes):
    records_to_insert = (InvoiceId, lineNo, ServId, EmpId, ServiceDate, HourlyOfService, Notes)
    sql_insert_service = """ INSERT INTO `serviceinvoices` (InvoiceId, lineNo, ServId, EmpId, ServiceDate, HourlyOfService, Notes) 
        VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql_insert_service, records_to_insert)
    conn.commit

#Create an empty Invoice with today's date 
def createInvoice(customer_):
    cur.execute("SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'egcleani_EG_Cleaning' AND TABLE_NAME = 'Invoices'")
    invoiceId = cur.fetchone()
    invoiceId = invoiceId[0]
    received = 0
    invoiceDate = datetime.today().strftime('%Y-%m-%d')
    customer = customer_
    paymentType = "E-Transfer"
    
    records_to_insert = (invoiceId, customer, invoiceDate, paymentType, received)

    sql_create_invoice = """ INSERT INTO Invoices (InvoiceId, Customer, InvoiceDate, PaymentType, Received) 
        VALUES (%s,%s,%s,%s,%s) """
    
    cur.execute(sql_create_invoice, records_to_insert)
    conn.commit()
    
#Get next line to insert each Service in one unique line
def getNextLine(invId):
    cur.execute("SELECT lineNo FROM serviceinvoices WHERE InvoiceId = %s ORDER BY lineNo DESC LIMIT 1" % (invId))
    lineNum = cur.fetchone()
    if not lineNum:
        return 1
    else:
        lineNum = lineNum[0] + 1
    return lineNum

#Get all Services IDs types of services provides? 
def getServId():
    cur.execute("SELECT ServId FROM Services")
    services = cur.fetchall()
    services = [ i[0] for i in services ] #Clear ID numbers
    i = 1
    print("Which service would you like to choose?")
    for row in services:
        print(i, " - ", row)
        i += 1
    
    #Loop to pick only valid data
    option = input("Enter a valid option: \n")
    service = services[int(option)-1]
    return service

#Get the last invoice ID UNPAID for that specific customer
def getOpenInvoice(customer):
    cur.execute("SELECT InvoiceID FROM Invoices WHERE Received = 0 AND Customer = %s ORDER BY 1 DESC LIMIT 1" % customer)
    invoice = cur.fetchone()
    if not invoice:
        createInvoice(customer)
    else: 
        invoice = invoice[0]
    return invoice

#If no date typed return todays date, else return dated typed
def getDate():
    today = input("Service provided in which date? ENTER FOR TODAY'S DATE\n")
    if not today:
        return datetime.today().strftime('%Y-%m-%d')
    else:
        return today
    
#Insert a service into unpaid invoice
def postService():
    customer = getCustId()
    invoice = getOpenInvoice(customer)
    emp = getEmpId()
    servDate = getDate()
    hoursWorked = input("How many hours worked? Eg. 3.00\n")
    line = getNextLine(invoice)
    note = input("Notes: ")
    service = getServId()
        
    print("Service inserted successfully")
    insertServiceInvoices(invoice, line, service, emp, servDate, hoursWorked, note)
    conn.commit()
    
#Insert expenses to database
def insertExpense():
    cur.execute("SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'egcleani_EG_Cleaning' AND TABLE_NAME = 'expenses'")
    expId = cur.fetchone()
    expId = expId[0]
    
    provider = input("Who is the provider? \n")
    desc = input("Receipt description: \n")
    price = input("What is it price? \n")
    expDate = getDate()
    
    cur.execute("SELECT SUBSTRING(COLUMN_TYPE,5) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='egcleani_EG_Cleaning' AND TABLE_NAME='expenses' AND COLUMN_NAME='categories'" )
    categories = cur.fetch_all()
    
    print("Which categories this receipt belongs to?")
    i = 1
    for row in categories:
        print(i, " - ", categories(row))
        i += 1
    
    category = input("Choose one: ")
    category = categories(category)
    print(categories)
    print(category)
    
    records_to_insert = (expId, provider, category, desc, price, expDate)
    sql_insert_expense = ("INSERT INTO `expenses` (`expId`, `provider`, `categories`, `expDesc`) VALUES (%s, %s, %s, %s)")
    
    cur.execute(sql_insert_expense, records_to_insert)
    conn.commit()
    print()

#Get all customers
def displayCustomers():
    select_query = ("SELECT * FROM Customer")
    cur.execute(select_query)
    customers = cur.fetchall()
#                 customers = [ i[0] for i in customers  ]
    print("Total of customers is:", cur.rowcount)
    print("Printing each customer information")
    print("ID:\t", "Name:\t\t\t\t", "Address:\t\t\t", "Phone:\t\t\t", "Email:\t\t", "Referral:")
    for row in customers:
        
        print(row[0], "\t", row[1], row[2].ljust(25), row[3].ljust(30), row[4].ljust(20), row[6].ljust(25), row[8])
        
#Get all employees
def displayEmployees():
    select_query = ("SELECT * FROM Employee")
    cur.execute(select_query)
    customers = cur.fetchall()
#                 customers = [ i[0] for i in customers  ]
    print("Total of Employee is:", cur.rowcount)
    print("Printing each customer information")
    print("ID:\t", "Name:\t\t\t\t", "Address:\t\t\t", "Phone:\t\t\t", "Email:\t\t", )
    for row in customers:
        
        print(row[0], "\t", row[1], row[2].ljust(25), row[3].ljust(30), row[4].ljust(20), row[6].ljust(25))  
#Menu to choose what to do

#Get employee email
def getEmpEmail():
    emp = getEmpId()

    select_query = ("SELECT empEmail FROM Employee WHERE EmpId = %s" % emp)
    cur.execute(select_query)
    email = cur.fetchone()
    email = email[0]
    return email
