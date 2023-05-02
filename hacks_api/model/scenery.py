from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import json
from PIL import Image
import sqlite3
import io
from pathlib import Path
from sqlalchemy import Column, Integer, String, Text, LargeBinary

# place your model code here
# you can use the code we showed in our lesson as an example

# make sure you put initial data here as well
# EXTRA CREDIT: make the placing of data more efficient than our method shown in the lesson

class Scenery(db.Model):
    __tablename__ = "scenery"

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _location = db.Column(db.String(255), nullable=False)
    _dateBuilt = db.Column(db.String(255), nullable=False)
    _image = db.Column(db.Text, nullable=False)

    def __init__(self, name, location, dateBuilt):
        self._name = name
        self._location = location
        self._dateBuilt = dateBuilt
   
    @property
    def name(self):
        return self._name
  
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def location(self):
        return self._location
  
    @location.setter
    def location(self, location):
        self._location = location

    @property
    def dateBuilt(self):
        return self._dateBuilt
  
    @dateBuilt.setter
    def dateBuilt(self, dateBuilt):
        self._dateBuilt = dateBuilt

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "dateBuilt": self.dateBuilt
        }

    # 
    # Converts Leaderboard to string values
    #                
    def __str__(self):
        return json.dumps(self.read())

    # 
    # Creates Leaderboard database
    #                
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # 
    # Updates Leaderboard DB rows for points and user data
    #                
    def update(self, name="", location="", dateBuilt=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(location) > 0:
            self.location = location
        if len(dateBuilt) > 0:
            self.dateBuilt = dateBuilt
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def initSceneries():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        p1 = Scenery(name="Chichen Itza", location="Mexico", dateBuilt="400s AD")
        p2 = Scenery(name="Great Wall of China", location="China", dateBuilt="220 BC")
        p3 = Scenery(name="Christ the Redeemer", location="Brazil", dateBuilt="1931")
        p4 = Scenery(name="Taj Mahal", location="India", dateBuilt="1653")
        places = [p1, p2, p3, p4]

        """Builds sample user/note(s) data"""
        for p in places:
            try:
                '''add user to table'''
                object = p.create()
                print(f"Created new uid {object.name}")
                db.session.add(p)
                db.session.commit()
            except:
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {p.name}, or error.")

initSceneries()