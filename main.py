# if these are not showing up, do pip install (the specific library that is missing)
# ex: if flask_cors is not showing, do "pip install flask_cors" and "pip install cors"

from flask_cors import CORS
from hacks_api.__init__ import app, db

from hacks_api.api.imagesapi import images_api
from hacks_api.model.image import initImages
from hacks_api.model.scenery import initSceneries
# from hacks_api.model.scenery2 import create_images
app.register_blueprint(images_api)

@app.before_first_request
def init_db():
        # create_images()
        initImages()
        initSceneries()



if __name__ == "__main__":
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8199")
