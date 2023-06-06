import unittest
from app import create_app
from extensions import db
from config import TestConfig

# Carry out unit tests using py and testing APIs using Flask
#Create a Test Case

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        #Test Client is an interface flask gives us to help test the application - make different requests for different routes
        self.client=self.app.test_client(self)

        with self.app.app_context(): 
            # db.init_app(self.app)

            db.create_all()

    #Create a test
    def test_hello_world(self):
        #what I'll get as the response from using my test client
        hello_response = self.client.get("/recipe/hello")
        json = hello_response.json
        # print(json)
        #use assert methods to compare
        self.assertEqual(json, {"message": "Hello World"})

    def test_signup(self):
        signup_res = self.client.post("/auth/signup",
            #Specify data we will send as JSON to the api
            json = {
                "username" : "testuser",
                "email" : "testuser@gmail.com",
                "password" : "password"}
        )

        status_code = signup_res.status_code

        self.assertEqual(status_code, 201)
        # print(status_code)

    def test_login(self):
        signup_res = self.client.post("/auth/signup",
            #Specify data we will send as JSON to the api
            json = {
                "username" : "testuser",
                "email" : "testuser@gmail.com",
                "password" : "password"}
        )
        mes = signup_res.json
        # print(mes)
        login_res = self.client.post("/auth/login",
            json = {
                "username" : "testuser",
                "password" : "password"
            }

        )
        status_code = login_res.status_code
        self.assertEqual(status_code, 200)

        json = login_res.json

        # print(json)

    def test_get_all_recipes(self):
        """TEST GETTING ALL RECIPES"""
        response = self.client.get("/recipe/recipes")
        # print(response.json)

        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_one_recipe(self):
        id = 1
        response = self.client.get(f"/recipe/recipe/{id}")

        status_code = response.status_code

        self.assertEqual(status_code, 404)

        # print(status_code)

    def test_create_recipe(self):
        signup_res = self.client.post("/auth/signup",
            #Specify data we will send as JSON to the api
            json = {
                "username" : "testuser",
                "email" : "testuser@gmail.com",
                "password" : "password"}
        )
        mes = signup_res.json
        # print(mes)
        login_res = self.client.post("/auth/login",
            json = {
                "username" : "testuser",
                "password" : "password"
            }

        )
        access_token = login_res.json["access token"]
        #Pass access token with the request of creating the recipe
        create_recipe_res = self.client.post("/recipe/recipes",
            json = {
                "title" : "Test Cake",
                "description" : "Test Description"
            },
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }
        )
        status_code = create_recipe_res.status_code
        # print(create_recipe_res.json)
        self.assertEqual(status_code, 201)

    def test_update_recipe(self):
        signup_res = self.client.post("/auth/signup",
            #Specify data we will send as JSON to the api
            json = {
                "username" : "testuser",
                "email" : "testuser@gmail.com",
                "password" : "password"}
        )
        # mes = signup_res.json
        # print(mes)
        login_res = self.client.post("/auth/login",
            json = {
                "username" : "testuser",
                "password" : "password"
            }

        )
        access_token = login_res.json["access token"]
        #Pass access token with the request of creating the recipe

        create_recipe_res = self.client.post("/recipe/recipes",
            json = {
                "title" : "Test Pizza",
                "description" : "Test Hawaaian Pizza Description"
            },
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }
        )

        create_recipe_res = self.client.post("/recipe/recipes",
            json = {
                "title" : "Test Cake",
                "description" : "Test Description"
            },
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }
        )

        id = 2
        update_recipe_res = self.client.put(f"/recipe/recipe/{id}",
            json = {
                "title" : "Test Cookies",
                "description" : "Test Updated from Test Cake"
            },
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }
        )
        status_code = update_recipe_res.status_code
        self.assertEqual(status_code, 200)

        get_one = self.client.get(f"/recipe/recipe/1")
        get_two = self.client.get(f"/recipe/recipe/2")
        print(get_one.json)
        print(get_two.json)        

    def test_delete(self):
        signup_res = self.client.post("/auth/signup",
            #Specify data we will send as JSON to the api
            json = {
                "username" : "testuser",
                "email" : "testuser@gmail.com",
                "password" : "password"}
        )
        # mes = signup_res.json
        # print(mes)
        login_res = self.client.post("/auth/login",
            json = {
                "username" : "testuser",
                "password" : "password"
            }

        )
        access_token = login_res.json["access token"]
        #Pass access token with the request of creating the recipe

        create_recipe_res = self.client.post("/recipe/recipes",
            json = {
                "title" : "Test Pizza",
                "description" : "Test Hawaaian Pizza Description"
            },
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }
        )

        create_recipe_res = self.client.post("/recipe/recipes",
            json = {
                "title" : "Test Cake",
                "description" : "Test Description"
            },
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }
        )
        id = 2
        delete_recipe_res = self.client.delete(f"/recipe/recipe/{id}",
            headers = {
                "Authorization" : f"Bearer {access_token}"
            }     
        )
        print(delete_recipe_res.json)
        status_code = delete_recipe_res.status_code
        self.assertEqual(status_code, 200)

        

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

#Test-Runner -> helps discover the tests written and run them
if __name__ == "__main__":
    unittest.main()

