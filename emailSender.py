import smtplib, ssl, sys

sys.path.append('C:\\Users\\Erik Gabril\\Desktop\\MySQL_Python\\SQL_Python_Project\\test')
import datetime

from test import *
#today = datetime.today().strftime('%Y-%m-%d')
# today = today.split("-")

# print(today)
print("Starting app...")
def connect():
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "erikgsilva8@gmail.com"
    password = input("Type your password for " + sender_email + " to send email: ")

    # Create a secure SSL context
    thisContext = ssl.create_default_context()

    emp = getEmpId()
    receiver_email = getEmpEmail(emp)
    employee = getEmpName(emp)
    week = datetime.date(2019, 6, 6).isocalendar()[1]
    message = 'Subject: {}\n\n{}'.format("Schedule for week: " + str(week), """\
    Hi """ + employee + """
        Here is your schedule for the """ + str(week) + """ 
    This message is sent from Python.""")
    SECURITY_EMAIL_SENDER = 'erikgsilva8@gmail.com'
    
    
     
    # Try to log in to server and send email
    try:
        # Secure the connection
        # TODO: Send email here
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=thisContext) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

if __name__ == '__main__':
    connect()
    print("End of Program")