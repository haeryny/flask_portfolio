""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _nameOfStudent = db.Column(db.String(255), unique=False, nullable=False)
    _nameOfClass = db.Column(db.String(255), unique=True, nullable=False)
    _nameOfHomework = db.Column(db.String(255), unique=True, nullable=False)
    _dateDue = db.Column(db.String(255), unique=True, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, nameOfStudent, nameOfClass, nameOfHomework, dateDue):
        self._nameOfStudent = nameOfStudent    # variables with self prefix become part of the object, 
        self._nameOfClass = nameOfClass
        self._nameOfHomework = nameOfHomework
        self._dateDue = dateDue

    # a name getter method, extracts name from object
    @property
    def nameOfStudent(self):
        return self._nameOfStudent
    
    # a setter function, allows name to be updated after initial object creation
    @nameOfStudent.setter
    def nameOfStudent(self, nameOfStudent):
        self._nameOfStudent = nameOfStudent

    # a name getter method, extracts name from object
    @property
    def nameOfClass(self):
        return self._nameOfClass
    
    # a setter function, allows name to be updated after initial object creation
    @nameOfClass.setter
    def nameOfClass(self, nameOfClass):
        self._nameOfClass = nameOfClass
    
    # a getter method, extracts email from object
    @property
    def nameOfHomework(self):
        return self._nameOfHomework
    
    # a setter function, allows name to be updated after initial object creation
    @nameOfHomework.setter
    def nameOfHomework(self, nameOfHomework):
        self._nameOfHomework = nameOfHomework
        
        # a name getter method, extracts name from object
    @property
    def dateDue(self):
        return self._dateDue
    
    # a setter function, allows name to be updated after initial object creation
    @dateDue.setter
    def dateDue(self, dateDue):
        self._dateDue = dateDue
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "nameOfStudent": self.nameOfStudent,
            "nameOfClass": self.nameOfClass,
            "nameOfHomework": self.nameOfHomework,
            "dateDue": self.dateDue,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, nameOfStudent="", nameOfClass="", nameOfHomework="", dateDue=""):
        """only updates values with length"""
        if len(nameOfStudent) > 0:
            self.nameOfStudent = nameOfStudent
        if len(nameOfClass) > 0:
            self.nameOfClass = nameOfClass
        if len(nameOfHomework) > 0:
            self.nameOfHomework(nameOfHomework)
        if len(dateDue) > 0:
            self.dateDue = dateDue
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(nameOfStudent='Sean Y', nameOfClass='APCSP', nameOfHomework='Make A Table', dateDue='1/22/23')
    u2 = User(nameOfStudent='Ellie P', nameOfClass='AP Bio', nameOfHomework='Portfolio', dateDue='1/23/23')
    u3 = User(nameOfStudent='Kaylee H', nameOfClass='APCSP', nameOfHomework='API', dateDue='1/25/23')
    u4 = User(nameOfStudent='Theo H', nameOfClass='AP Calc', nameOfHomework='Pg 123, #1, 2, 3', dateDue='1/20/23')

    users = [u1, u2, u3, u4]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.nameOfStudent + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.nameOfStudent}")
            