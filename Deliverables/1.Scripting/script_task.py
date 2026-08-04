import csv
from email_validator import validate_email, EmailNotValidError
with open("./scripting/data.txt", "r") as file:
    reader = csv.reader(file)

    ## skip first row of name , email , user_id
    next(reader) 
    for row in reader:
        # valuser_idate the user_id
        id_str = row[-1].strip()
        try:
            user_id = int(id_str)
        except ValueError:
            print(f"Warning: Invalid user_id -> {id_str}")
            continue 

        # valuser_idate email
        try:
            email = row[-2].strip()
            validate_email(email)
        except EmailNotValidError:
            print(f"Warning: Invalid Email -> {email}")
            continue 
        # remuser_ider of the user_id
        reminder = user_id % 2
        if reminder == 0 :
            print(f"the {user_id} of {email} is even number")
        else:
            print(f"the {user_id} of {email} is odd number")
            

