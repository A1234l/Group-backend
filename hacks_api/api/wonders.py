import base64
from flask import current_app
from sqlalchemy import Column, Integer, String, Text
from __init__ import db

class Images(db.Model):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    data = Column(Text, nullable=False)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"<Images(id={self.id})>"

    def to_dict(self):
        return {"id": self.id}

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        with current_app.app_context():
            image_data = base64.b64encode(self.data).decode("utf-8")
        return {"image": image_data}
