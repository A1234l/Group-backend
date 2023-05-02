from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import base64
from pathlib import Path
from model.scenery2 import Images, db


@app.route('/images', methods=['POST'])
def upload_image():
    image_data = request.files.get('image').read()
    image = Images(path="", x_coord=0, y_coord=0, difficulty=1)
    image_data_encoded = base64.b64encode(image_data).decode('utf-8')
    image.path = f"data:image/png;base64,{image_data_encoded}"
    db.session.add(image)
    db.session.commit()
    return jsonify({"id": image.id})


@app.route('/images', methods=['GET'])
def get_images():
    images = Images.query.all()
    response_data = [image.to_dict() for image in images]
    return jsonify(response_data)


@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Images.query.get(image_id)
    if not image:
        return Response(status=404)
    return jsonify(image.read_image())


def create_images():
    images_directory = Path("./images")
    for image_path in images_directory.glob("*.png"):
        image_data = image_path.read_bytes()
        image_data_encoded = base64.b64encode(image_data).decode('utf-8')
        image = Images(path=f"data:image/png;base64,{image_data_encoded}", x_coord=0, y_coord=0, difficulty=1)
        image.create()


