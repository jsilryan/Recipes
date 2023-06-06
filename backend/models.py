#Build sqlalchemy models
from extensions import db

"""
class recipe:
    id: int primary key
    title: str
    description: str (text)

"""

class Recipe(db.Model):
    #will create sql code after running db.create_all() in flask shell
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    #CRUD operations
    def __repr__(self):
        return f"<Recipe {self.title} >"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def title_update(self, title):
        self.title = title
        db.session.commit() #saving to the database

    def des_update(self, description):
        self.description = description
        db.session.commit() #saving to the database

"""
class User:
    id: int primary key
    username: str
    email: string
    password: string

"""

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    email =  db.Column(db.String(50), nullable = False)
    password = db.Column(db.Text(), nullable = False)

    def __repr__(self): #string representation of the object - f string
        return f"<User {self.username} >"

    def save(self):
        db.session.add(self)
        db.session.commit()
    #flask migrate:- Create a model on the database without losing data - install using pip install flask_migrate
    #Creating database - $env:FLASK_APP = "main.py"; flask shell
    #Crate migrate repository - flask db init
    #Name your main file as app.py 
    #flask db migrate -m "add user table" => Creates the table and a migration for it
    #Setting the migration will update the new table into the database - check new sql data of the table on migrations/version/...
    #It will have the sql schema commands to create into the database
    #After creating the commands, you create it in the database using - flask db upgrade - It will upgrade to the current version created
    #$env:FLASK_APP ="app.py" => powershell; export FLASK_APP = "app.py" => Linux; set FLASK_APP = "app.py" => cmd
    #JWT for authentication
    #Expected data from UI - suggest data our api will receive
    #Flaskrestx => api.expect declarator and pass in the model serializer
    #Decorate the function with the api.expect -> above marshal_with
    #In the swagger UI, /docs, the api.expect creates a payload in the post requests that helps see what the server should expect
    #Werkzeug - used for security; has various functions that help check and hash passwords
    #After creating the signup route and class, for password we will use werkzeug.security; To understand the logic, Open terminal and type:
    #password ="password"
    #from werkzeug.security import generate_password_hash, check_password_hash
    #pwd_hash = generate_password_hash(password)
    #pwd_hash -> will be the password saved in the database
    #check_password_hash(pwd_has, "password")
    #If it returns True: the password matches the hash 
    #If I am not returning the object created eg new_user, I do not need to decorate the def function using marshal_with
    #I can jsonify({"message": "User created successfully"})
    #Next you use JWT_extended to carry out JWT authentication
    #To connect to the server:- jwt_required - helps protect routes
    #Missing authorization header in Swagger API - go to header and add a new header: Authorization : Bearer --access code--
    #We can create various versions of the app -> instead of having one file that has all the logic of the app,
    #we'll create the Application Factory Function that will create the app and return the app.
    #JWT_Required -> use signup and login in order to get access to the token to use to access the route