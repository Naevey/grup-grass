from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from __init__ import app

# Define variable to define type of database (sqlite), and name and location of myDB.db
dbURI = 'sqlite:///mogel/myDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
# Create SQLAlchemy engine to support SQLite dialect (sqlite:)
db = SQLAlchemy(app)
Migrate(app, db)

class Students(db.Model):

    studentID = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.Text)

    # constructor of a Event object, initializes of instance variables within object
    def __init__(self, firstname, lastname, title, description):
        self.firstname = firstname
        self.lastname = lastname
        self.title = title
        self.description = description

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Events(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Events table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "studentID": self.studentID,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "title": self.title,
            "description": self.description
        }

    # CRUD update: updates events name, description, etc
    # returns self
    def update(self, firstname, lastname="", title="", description=""):
        """only updates values with length"""
        if len(firstname) > 0:
            self.firstname = firstname
        if len(lastname) > 0:
            self.lastname = lastname
        if len(title) > 0:
            self.title = title
        if len(description) > 0:
            self.description = description
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def student_tester():
    print("--------------------------")
    print("Seed Data for Table: Students")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Students(firstname='everit', lastname='cheng', title='hungry caterpillar', description="This is a caterpillar")
    u2 = Students(firstname='mathew', lastname='cow',title='jim', description="This is an innuendo")
    u3 = Students(firstname='erig', lastname='peter',title='antony vo', description="peter")
    table = [u1, u2, u3]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate url, or error: {row.url}")

def student_printer():
    print("------------")
    print("Table: Students with SQL query")
    print("------------")
    result = db.session.execute('select * from students')
    print(result.keys())
    for row in result:
        print(row)

if __name__ == "__main__":
    student_tester()  #
    student_printer() #