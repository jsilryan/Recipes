from flask import Flask, request, jsonify, make_response
from flask_restx import Resource, Namespace, fields #framework used to build the API
from models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_jwt_extended import (JWTManager, create_access_token, 
create_refresh_token, jwt_required, get_jwt_identity
)

#namespace - similar to a blueprint

auth_ns = Namespace("auth", description = "A namespace for the Authentication")

signup_model = auth_ns.model(
    "Sign-Up",
    {
        # "id" : fields.Integer(),
        "username" : fields.String(),
        "email" : fields.String(),
        "password": fields.String()
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "username": fields.String(),
        "password": fields.String()
    }
)


@auth_ns.route('/signup')
class SignUp(Resource):
    # @api.marshal_with(signup_model)
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        #check if user exists
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message" : f"User with username {username} already exists!"})
        new_user = User (
            username = data.get("username"),
            email = data.get("email"),
            password = generate_password_hash(data.get("password"))
        )
        new_user.save()
        return make_response(jsonify({"message": "User created successfully"}), 201)


@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        
        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            #give the authenticated user a refresh token and access token
            access_token = create_access_token(identity = db_user.username) #Always hides the identity of a user who it belongs to
            refresh_token = create_refresh_token(identity = db_user.username)

            return make_response(jsonify(
                {
                    "access token" : access_token,
                    "refresh token" : refresh_token
                }
            ), 200)

#Create a route to create refresh tokens - help create new access tokens incase the access token has expired
@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh = True) #will require refresh token
    def post(self):
        #Get current user -> jwt_identity
        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity = current_user)

        return make_response(jsonify({"access token" : new_access_token}), 200)
        #Authorization - Bearer (Refresh token of a logged in user)