from flask import url_for
from werkzeug.utils import redirect

from __init__ import login_manager, db
from model import Students
from flask_login import current_user, login_user, logout_user


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def students_all():
    """  May have some problems with sql in deployment
    if random.randint(0, 1) == 0:
        table = users_all_alc()
    else:
        table = users_all_sql()
    return table
    """

    return students_all_alc()


# SQLAlchemy extract all users from database
def students_all_alc():
    table = Students.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Native SQL extract all users from database
def students_all_sql():
    table = db.session.execute('select * from students')
    json_ready = sqlquery2_2_list(table)
    return json_ready


# ALGORITHM to convert the results of an SQL Query to a JSON ready format in Python
def sqlquery2_2_list(rows):
    out_list = []
    keys = rows.keys()  # "Keys" are the columns of the sql query
    for values in rows:  # "Values" are rows within the SQL database
        row_dictionary = {}
        for i in range(len(keys)):  # This loop lines up K, V pairs, same as JSON style
            row_dictionary[keys[i]] = values[i]
        row_dictionary["query"] = "by_sql"  # This is for fun a little watermark
        out_list.append(row_dictionary)  # Finally we have a out_list row
    return out_list


# SQLAlchemy extract users from database matching term
def students_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Students.query.order_by(Students.name).filter((Students.name.ilike(term)) | (Students.email.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single user from database matching ID
def student_by_id(userid):
    """finds User in table matching userid """
    return Students.query.filter_by(userID=userid).first()


# SQLAlchemy extract single user from database matching email
def student_by_firstname(firstname):
    """finds User in table matching email """
    return Students.query.filter_by(firstname=firstname).first()


# check credentials in database
def is_user(firstname, lastname):
    # query email and return user record
    user_record = student_by_firstname(firstname)
    # if user record found, check if password is correct
    return user_record and Students.is_password_match(user_record, lastname)


# login user based off of email and password
def login(firstname, lastname):
    # sequence of checks
    if current_user.is_authenticated:  # return true if user is currently logged in
        return True
    elif is_user(firstname, lastname):  # return true if email and password match
        user_row = student_by_firstname(firstname)
        login_user(user_row)  # sets flask login_user
        return True
    else:  # default condition is any failure
        return False


# this function is needed for Flask-Login to work.
@login_manager.user_loader
def user_loader(user_id):
    """Check if user login status on each page protected by @login_required."""
    if user_id is not None:
        return Students.query.get(user_id)
    return None


# Authorise new user requires user_name, email, password
def authorize(firstname, lastname):
    if is_user(firstname, lastname):
        return False
    else:
        auth_user = Students(
            firstname=firstname,
            lastname=lastname,
        )
        # encrypt their password and add it to the auth_user object
        auth_user.create()
        return True


# logout user
def logout():
        logout_user()  # removes login state of user from session
        return redirect(url_for('crud'))
# Test some queries from implementations above
if __name__ == "__main__":

    # Look at table
    print("Print all at start")
    for student in students_all():
        print(student)
    print()

    """ Password Lookup Sample Code """
    # Expected success on Email and Password lookup
    firstname = "Thomas Edison"
    lastname = "tedison@example.com"
    psw = "123toby"
    print(f"Check is_user with valid email and password {firstname}, {psw}", is_user(lastname, psw))

    # Expected failure on Email and Password lookup
    psw1 = "1234puffs"
    print(f"Check is_user with invalid password: {firstname}, {psw1}", is_user(lastname, psw1))

    """ Authorization Screen Sample Code"""
    # Expected failure as user exists
    print(f"Check authorize with existing email and password: {firstname}, {psw}", authorize(firstname, lastname, psw))

    # Expected success as user does not exist
    firstname1 = "Coco Puffs"
    lastname1 = "puffs@example.com"
    print(f"Check authorize with new email and password: {firstname1}, {psw1}", authorize(firstname1, lastname1, psw1))

    # Look at table
    print()
    print("Print all at end")
    for student in students_all():
        print(student)

    # Clean up data from run, so it can run over and over the same
    user_record = student_by_firstname(lastname1)
    user_record.delete()
