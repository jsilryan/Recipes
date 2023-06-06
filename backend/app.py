from flask import Flask, request, jsonify
from flask_restx import Api,Resource, fields, Namespace 
from decouple import config
from config import DevConfig
from models import Recipe, User
from extensions import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipe import recipe_ns
from auth import auth_ns
from flask_cors import CORS

def create_app(config):
    app = Flask(__name__)
    
    app.config.from_object(config)

    CORS(app)

    db.init_app(app) #registers sqlalchemy to work with the app(current application)

    migrate = Migrate(app,db)

    JWTManager(app) #Makes the flask_jwt to work with the app 

    api = Api(app, doc = "/docs") #instance of the API, doc is the url we want our documentation

    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)
    #helps interact with the database
    @app.shell_context_processor 
    def make_shell_context():
        return {
            "db": db,
            "Recipe": Recipe,
            "user" : User
        }
    return app

if __name__ == "__main__":
    app = create_app(DevConfig)
    app.run()


# if __name__ == "__main__": #Run the server
#     app.run()
# app = Flask(__name__)
# app.config.from_object(DevConfig)

# db.init_app(app) #registers sqlalchemy to work with the app(current application)

# migrate = Migrate(app,db)

# JWTManager(app) #Makes the flask_jwt to work with the app 

# api = Api(app, doc = "/docs") #instance of the API, doc is the url we want our documentation



# @api.route('/hello') 
# #defines all the routes/ methods to be carried out on the route
# class HelloResource(Resource):
#     def get(self):
#         return {"message" : "Hello World"}


# if __name__ == "__main__": #Run the server
#     app.run()

# #Context processor - access model and db processor from terminal - injects new variable into a context of a template
# # @app.context_processor
# # def inject_now():
# #     return {'now': datetime.utcnow()}
# # Can be injected as {{now}}

# #helps interact with the database
# @app.shell_context_processor 
# def make_shell_context():
#     return {
#         "db": db,
#         "Recipe": Recipe
#     }
#set FLASK_APP=main.py
#pip freeze > requirements.txt - create a requirements file in backend with pip - shows vaious dependencies for the project
#Flask-JWT-extended - create login and sign up functionality - need a user model - create in model.py
