from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import base64
from pathlib import Path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f'<Image(id={self.id})>'

    def to_dict(self):
        return {"id": self.id}

    def read(self):
        image_data = base64.b64encode(self.data).decode('utf-8')
        return {"image": image_data}

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


@app.route('/images', methods=['POST'])
def upload_image():
    image_data = request.files.get('image').read()
    image = Image(data=image_data)
    db.session.add(image)
    db.session.commit()
    return jsonify({"id": image.id})


@app.route('/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    response_data = [image.read() for image in images]
    return jsonify(response_data)


def create_images():
    images_dir = Path('./images')
    for image_file in images_dir.glob('*.jpg'):
        with open(image_file, 'rb') as f:
            image_data = f.read()
        image = Image(data=image_data)
        db.session.add(image)
    db.session.commit()
