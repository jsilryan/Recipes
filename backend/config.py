from decouple import config #helps separate settings from code and you can do it without redeploying the code
import os

BASE_dir = os.path.dirname(os.path.realpath(__file__))

class Config:
    #configuration keys for flask
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)

class DevConfig(Config): #inherits from global config
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_dir,'dev.db') #database URI used for connection
    DEBUG = True #Access exceptions on the front end and see the error
    SQLALCHEMY_ECHO = True #SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.

class ProdConfig(Config):
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False #Prevents SQLAlchemy from generating any SQL scripts
    TESTING = True