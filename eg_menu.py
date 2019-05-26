import sys
sys.path.append('C:\\Users\\Erik Gabril\\Desktop\\MySQL_Python\\SQL_Python_Project\\queries')

from queries import *
# from eg_cleaning import postService
# from eg_cleaning import displayCustomers
# from eg_cleaning import displayEmployees

def menu():
    load = True
    menu = {}
    menu[0] = "Exit"
    menu[1] = "Add new customer" 
    menu[2] = "Add new service"
    menu[3] = "Display all customers"
    menu[4] = "Display all employees"
    menu[5] = "Send schedule"
    
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
        elif selection == '0':
            print("Goodbye...")
            load = False
        else: 
            print("Invalid option!")

if __name__ == '__main__':
    menu()
    print("End of Menu Program")