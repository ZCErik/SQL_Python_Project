def get_customer_details(id):
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    street = input("Street address: ")
    phone = input("Phone Number: ")
    email = input("Email: ")
    note = input("Notes: ")
    ref = input("Referral: ")


    return id, firstName, lastName,street, phone, email, note, ref


# Insert POSTAL CODE
def get_postal_code_details():
    zip_code = input("Please enter Postal Code: Eg. A1B 2C3\n")
    city = input("Please enter the City: \n")
    region = input("Please enter the Region: \n")

    return zip_code, city, region
