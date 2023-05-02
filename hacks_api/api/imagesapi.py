from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from __init__ import db
from hacks_api.model.image import Images
import os, random
import base64

images_bp = Blueprint("images", __name__, url_prefix='/api/images')
images_api = Api(images_bp)

def getImage():
    images = Images.query.all()
    image = random.choice(images)
    return image

class ImagesAPI:
    class _ReadImages(Resource):
        def get(self):
            image = getImage()
            json_data = {}
            if image:
                image_path = "hacks_api" + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))[2:][:-1]
                json_data["xCoord"] = image.xCoord
                json_data["yCoord"] = image.yCoord
            return jsonify(json_data)
        
    class _CreateImages(Resource):
        def post(self):
            body = request.get_json(force=True)
            name = body.get("name")
            data = body.get("data")

            if(not name):
                return "No Name Found"
            if(not data):
                return "No Data Found"
            
            user = Images(name=name, data=data)

            if(user.create() != None):
                return user.read()
            
            return "User creation error, probably a duplicate"
    
    class _UpdateImages(Resource):
        def put(self):
            body = request.get_json(force=True)
            name = body.get("name")
            data = body.get("data")

            if(not name):
                return "No Name Found"
            if(not data):
                return "No Data Found"
            
            try:
                user = getImage(name)
            except:
                return "No User Found"

            if(data):
                try:
                    user.update(data=data)
                    return f"User with name {user.name} updated with data {data}"
                except:
                    return "Update error"
            
            return "Some weird error"
        
    class _DeleteImages(Resource):
        def delete(self):
            body = request.get_json(force=True)
            name = body.get("name")

            if(not name):
                return "No Name Found"
            
            try:
                user = getImage(name)
            except:
                return "No User Found"
            
            user.delete()

            return f"User with name {name} deleted"

        
    images_api.add_resource(_ReadImages, '/readImage')
    images_api.add_resource(_CreateImages, '/createImage')
    images_api.add_resource(_UpdateImages, '/updateImage')
    images_api.add_resource(_DeleteImages, '/deleteImage')