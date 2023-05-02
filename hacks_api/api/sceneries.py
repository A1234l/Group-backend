from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 
from datetime import datetime
from model.scenery import Scenery

# Create score blueprint for API
sceneries_bp = Blueprint("sceneries_bp", __name__, url_prefix='/api/scenery')
# Score API derived from blueprint
sceneries_api = Api(sceneries_bp)

# Define class for the API
class SceneryAPI:
    # Define class to create a user using the POST method
    class SceneryCreate(Resource):    
        def post(self):
            # Gets the data from postman or frontend
            data = request.get_json()

            name = data.get('name')
            if name is None:
                return {'message': f'name does not exist, or is missing'}, 210
                
            location = data.get('location')
            if location is None:
                return {'message': f'Location does not exist, or is missing'}, 210 
            
            dateBuilt = data.get('dateBuilt')
            if dateBuilt is None:
                return {'message': f'Date built does not exist, or is missing'}, 210 
            
            sob = Scenery(name=name, location=location, dateBuilt=dateBuilt)
            
            # CREATE operation: creates user
            user = sob.create()
            if user:
                # make_dict() function to return a dictionary for the user
                return jsonify(user.read())
            # returns error message if unable to return a dictionary
            return {'message': f'Processed {name}, there is likely a format error'}, 210

    # GET method displays the data from the API
    class SceneryListAPI(Resource):
        # def get(self) does the GET method
        def get(self):
            # Gets all the data from Score and returns a dictionary
            sceneries = Scenery.query.all()
            json_ready = [user.read() for user in sceneries]
            return jsonify(json_ready)

    # PUT method updates data in the API
    class SceneryUpdate(Resource):
        # def put(self) does the PUT method
        def put(self):
            # Gets the data from postman or frontend
            data = request.get_json()

            # Gets the username
            usernameData = data.get('username')

            # Gets the score, score is going to be updated
            scoreData = data.get('score')

            # Gets the user through the username
            userUpdating = Scenery.query.filter_by(_username = usernameData).first()
            if userUpdating:
                # Updates the score for the user
                userUpdating.update(score = scoreData)
                # Returns a dictionary to confirm that the score was updated
                return jsonify(userUpdating.read())
            else:
                # Error message if update fails
                return {'message': f'{usernameData} not found'}, 210

    # Delete method deletes data in the API
    class SceneryDelete(Resource):
        # def delete(self) does the DELETE method
        def delete(self):
            # Gets the data from postman or frontend
            data = request.get_json()

            # Gets the ID
            getID = data.get('id')

            # Gets the user through the ID
            historyDeleting = Scenery.query.get(getID)
            if historyDeleting:
                # Deletes the user according to its ID number
                historyDeleting.delete()
                return {'message': f'Profile #{getID} deleted'}, 210
            else:
                # Error message if delete fails
                return {'message': f'Profile #{getID} not found'}, 210
    
    # Endpoints, uses URL prefix and '/' to refer to different classes which corresponds to different methods
    sceneries_api.add_resource(SceneryCreate, '/addScenery')
    sceneries_api.add_resource(SceneryListAPI, '/sceneriesList')
    sceneries_api.add_resource(SceneryUpdate, '/updateScenery')
    sceneries_api.add_resource(SceneryDelete, '/deleteScenery')

