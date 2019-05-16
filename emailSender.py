import smtplib, ssl, sys

sys.path.append('C:\\Users\\Erik Gabril\\eclipse-workspace\\MySQL_Python')
import datetime

# import dataTest
# from dataTest import getEmpEmail
#today = datetime.today().strftime('%Y-%m-%d')
# today = today.split("-")

# print(today)

def connect():
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "erikgsilva8@gmail.com"
    receiver_email = "expertgeneralservices@gmail.com"
    password = input("Type your password: ")
    employee = "Michelle"
    week = datetime.date(2019, 5, 15).isocalendar()[1]
    print(week)
    message = """\
    Subject: Hi """, employee, """
        Here is your schedule for the following week
    This message is sent from Python."""
     
    # Create a secure SSL context
    thisContext = ssl.create_default_context()
     
    # Try to log in to server and send email
    try:
        # Secure the connection
        # TODO: Send email here
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted 
            server.starttls(context=thisContext)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
         
        
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 