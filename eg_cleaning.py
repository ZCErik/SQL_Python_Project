import mysql.connector
from datetime import datetime

def connect():
    """ Connect to MySQL database """

    try:
        # password = input("What is your password to connect to EG Cleaning?\n")
        conn = mysql.connector.connect(host='50.87.144.133',
                                       database='egcleani_EG_Cleaning',
                                       user='egcleani_erik',
                                       password='Erik0408')
        
        if conn.is_connected():
            print('Connected to MySQL database')
            cur=conn.cursor() 

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
            cur.execute("SELECT custId FROM Customer WHERE CustFirstNam LIKE ('%%%s%%') or CustLastNam LIKE ('%%%s%%')" % (name, name))
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
                
                return customer
            
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
            cur.execute("SELECT EmpId FROM Employee WHERE (EmpFirstNam LIKE ('%%%s%%') OR EmpLastNam LIKE ('%%%s%%'))" % (emp, emp))
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
            paymentType = input("How the customer is paying?\n")
            
            records_to_insert = (invoiceId, customer, invoiceDate, paymentType, received)

            sql_create_invoice = """ INSERT INTO Invoices (InvoiceId, Customer, InvoiceDate, PaymentType, Received) 
                VALUES (%s,%s,%s,%s,%s) """
            
            cur.execute(sql_create_invoice, records_to_insert)
            return conn.commit()
            
        #Get next line to insert each Service in one unique line
        def getNextLine(invId):
            cur.execute("SELECT lineNo FROM serviceinvoices WHERE InvoiceId = %s ORDER BY lineNo DESC LIMIT 1" % (invId))
            lineNum = cur.fetchone()
            if lineNum is None:
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

        #Get the last invoice ID UNPAID for that specific customer, if DOES NOT EXIST, Open and insert a service to invoice
        def getOpenInvoice(customer):
            cur.execute("SELECT InvoiceID FROM Invoices WHERE Received = 0 AND Customer = %s ORDER BY 1 DESC LIMIT 1" % customer)
            invoice = cur.fetchone()
            if invoice is None:
                createInvoice(customer)
                getOpenInvoice(customer)
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
            
        #Insert receipt expenses into MySQL
        def insertExpense():
            cur.execute("SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'egcleani_EG_Cleaning' AND TABLE_NAME = 'expenses'")
            expId = cur.fetchone()
            expId = expId[0]
            
            provider = input("Who is the provider? \n")
            desc = input("Receipt description: \n")
            price = input("What is it price? \n")
            expDate = getDate()
            
            cur.execute("SELECT SUBSTRING(COLUMN_TYPE,5) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='egcleani_EG_Cleaning' AND TABLE_NAME='expenses' AND COLUMN_NAME='categories'" )
            categories = cur.fetchall()
            categories = [ i[0] for i in categories ] #Clear ID numbers
            

            i = 1
            print("Which category this receipt belongs to?")
            
            category = []

            for row in categories:
                for x in row.split(","):
                    print(i, "-", x)
                    category.append(x)
                    i += 1 

            option = input("Enter a valid option: \n")
            category = category[int(option)-1]
            category = category.strip("',/\n")
            

            records_to_insert = (expId, provider, category, desc, price, expDate)
            sql_insert_expense = ("INSERT INTO `expenses` (`expId`, `provider`, `categories`, `expDesc`, `expPrice`, `expDate`) VALUES (%s, %s, %s, %s, %s, %s)")
            
            cur.execute(sql_insert_expense, records_to_insert)
            conn.commit()

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

        def menu():
            load = True
            menu = {}
            menu[0] = "Exit"
            menu[1] = "Add new customer" 
            menu[2] = "Add new service"
            menu[3] = "Display all customers"
            menu[4] = "Display all employees"
            menu[5] = "Send schedule"
            menu[6] = "Tests"
            menu[7] = "Add new expense"
            
            while load: 
                options = menu.keys()

                for entry in options: 
                    print(entry, menu[entry])
            
                selection=input("Please Select:\n") 
                if selection =='1': 
                    print("========== Register new Customer ==========")
                    registerCustomer()
                elif selection == '2': 
                    print("========== Register new Service ==========")
                    postService()
                elif selection == '3':
                    print("Finding all customers...")
                    displayCustomers()
                elif selection == '4':
                    print("Finding all Employees...")
                    displayEmployees()
                elif selection == '5':
                    print("Send schedule...")
                    print("Not working yet...")
                elif selection == '6':
                    print("Set up a test first.")
                    cust = getCustId()
                    print(cust)
                elif selection == '7':
                    print("Add any receipt here")
                    insertExpense()
                elif selection == '0':
                    print("Goodbye...")
                    load = False
                else: 
                    print("Invalid option!")

        #call menu function to run the program
        menu()

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