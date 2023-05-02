import base64

from sqlalchemy import Column, Integer, String, Text
from pathlib import Path
from __init__ import app, db


class Images(db.Model):
    __tablename__ = 'scenery2'
    id = Column(Integer, primary_key=True)
    path = Column(Text, unique=True, nullable=False)
    x_coord = Column(Integer, nullable=False)
    y_coord = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __init__(self, path, x_coord, y_coord, difficulty):
        self.path = path
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.difficulty = difficulty

    def __repr__(self):
        return f"<image(id='{self.id}', path='{self.path}', x_coord='{self.x_coord}', y_coord='{self.y_coord}', difficulty='{self.difficulty}')>"

    def to_dict(self):
        return {"id": self.id, "path": self.path, "x_coord": self.x_coord, "y_coord": self.y_coord, "difficulty": self.difficulty}

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {"path": self.path, "x_coord": self.x_coord, "y_coord": self.y_coord, "difficulty": self.difficulty}

    def update(self, path="", x_coord="", y_coord="", difficulty=""):
        if path:
            self.path = path
        if x_coord is not None:
            self.x_coord = x_coord
        if y_coord is not None:
            self.y_coord = y_coord
        if difficulty is not None:
            self.difficulty = difficulty
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def read_image(self):
        with open(self.path, "rb") as f:
            image_data = f.read()
        return {"image": base64.b64encode(image_data).decode("utf-8")}


def create_images():
    images_directory = Path("./images")
    for image_path in images_directory.glob("*.png"):
        image = Images(path=str(image_path), x_coord=0, y_coord=0, difficulty=1)
        image.create()
