from sqlalchemy import Column, Integer, String, Text, LargeBinary
from sqlalchemy.exc import IntegrityError
from pathlib import Path
from __init__ import app, db

class Images(db.Model):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    _imagePath = Column(Text, unique=True, nullable=False)
    _xCoord = Column(Integer, nullable=False)
    _yCoord = Column(Integer, nullable=False)
    _difficulty = Column(Integer, nullable=False)

    
    def __init__(self, imagePath, xCoord, yCoord):
        self._imagePath = imagePath
        self.xCoord = xCoord
        self.yCoord = yCoord

    def __repr__(self):
        return "<image(id='%s', imagePath='%s', xCoord='%s', yCoord='%s')>" % (
            self.id,
            self.imagePath,
            self.xCoord,
            self.yCoord
        )
    @property
    def imagePath(self):
        return self._imagePath

    @imagePath.setter
    def imagePath(self, value):
        self._imagePath = value

    @property
    def xCoord(self):
        return self._xCoord

    @xCoord.setter
    def xCoord(self, value):
        self._xCoord = value

    @property
    def yCoord(self):
        return self._yCoord

    @yCoord.setter
    def yCoord(self, value):
        self._yCoord = value

    def to_dict(self):
        return {"id": self.id, "imagePath": self._imagePath, "xCoord": self._xCoord, "yCoord": self._yCoord}

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
            "path": self.imagePath,
            "xCoord": self.xCoord,
            "yCoord": self.yCoord
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, path="", xCoord="", yCoord=""):
        """only updates values with length"""
        xCoord = int(xCoord)
        yCoord = int(yCoord)
        if path:
            self.imagePath = path
        if xCoord >= 0:
            self.xCoord = xCoord
        if yCoord >= 0:
            self.yCoord = yCoord
        db.session.commit()
        return self


    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def initImages():
    with app.app_context():
        db.create_all()
        image_dir = Path.cwd()/"images/"
        images_paths = [i.name for i in image_dir.iterdir()]
        images = [Images("images/" + image, 250, 250, 0) for image in images_paths]
        for image in images:
            try:
                image.create()
                print("Successfully added entry")
            except:
                db.session.remove()
                print("Error adding image: ", image.imagePath)

initImages()