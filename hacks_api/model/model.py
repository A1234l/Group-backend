from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import json
from PIL import Image
import io

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
    _image = db.Column(db.Image, nullable=False)

    def __init__(self, name, location, dateBuilt, image):
        self._name = name
        self._location = location
        self._dateBuilt = dateBuilt
        self._image = image
   
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

# Example added for image setter getter, someone please change it so it works
class ImagesAPI:
    class _EasyImages(Resource):
        def get(self):
            image = get_random_easy_image()
            json_data = {}
            if image:
                image_path = project_path + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))[2:][:-1]
                json_data["xCoord"] = image.xCoord
                json_data["yCoord"] = image.yCoord
            return jsonify(json_data)    

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "dateBuilt": self.dateBuilt,
            "image": self.image
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
    def update(self, name="", location="", dateBuilt="", image=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(location) > 0:
            self.location = location
        if len(dateBuilt) > 0:
            self.dateBuilt = dateBuilt
        if image:
            self.image = image
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def init_leaderboards():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        l1 = Leaderboard(username="bob", password="apple", pointsEasy=2, pointsMedium=5, pointsHard=3)
        l2 = Leaderboard(username="bobby", password="appley", pointsEasy=20, pointsMedium=50, pointsHard=30)
        l3 = Leaderboard(username="bobbert", password="appled", pointsEasy=200, pointsMedium=500, pointsHard=300)
        l4 = Leaderboard(username="bobruth", password="appler", pointsEasy=100, pointsMedium=300, pointsHard=500)
        leaderboards = [l1, l2, l3, l4]

        """Builds sample user/note(s) data"""
        for l in leaderboards:
            try:
                '''add user to table'''
                object = l.create()
                print(f"Created new uid {object.username}")
                db.session.add(l)
                db.session.commit()
            except:
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {l.username}, or error.")

init_leaderboards()