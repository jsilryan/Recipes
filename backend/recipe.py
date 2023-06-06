from flask import Flask, request, jsonify
from flask_restx import Namespace, Resource, fields
from models import Recipe
from flask_jwt_extended import jwt_required 

recipe_ns = Namespace("recipe", description =  "Recipes Namespace")

recipe_model= recipe_ns.model(
    "Recipe", #name of the model
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description": fields.String()
    }
) #model_serializer of a class to json format; can classify the fields as our model states 

@recipe_ns.route('/hello') 
#defines all the routes/ methods to be carried out on the route
class HelloResource(Resource):
    def get(self):
        return {"message" : "Hello World"}


@recipe_ns.route("/recipes")
class RecipesResources(Resource):
    @recipe_ns.marshal_list_with(recipe_model) #return a list of recipes; multiple objects
    def get(self):
        """Get all recipies"""
        #The recipes will be returned in SQLAlchemy format, therefore, we have to convert to JSON using the serializer
        recipes=Recipe.query.all()

        return recipes
    @recipe_ns.marshal_with(recipe_model)#returning 1 object
    @recipe_ns.expect(recipe_model)
    @jwt_required()
    def post(self):
        """Create a new recipe"""
        #first access data from the json using request object from flask; contains body, headers and any other data from frontend
        data = request.get_json() #get_json helps acquire data from the request from any client
 
        new_recipe = Recipe(
            title = data.get("title"),
            description = data.get("description")
        )
        new_recipe.save()

        return new_recipe,201 #created status code
            

#First get all recipes and convert to a list of recipes; 

#Get recipe by id
@recipe_ns.route("/recipe/<int:id>")
class RecipeResource(Resource):
    @recipe_ns.marshal_with(recipe_model) #Return the recipe as JSON
    def get(self, id):
        """Get a recipe by id"""
        recipe = Recipe.query.get_or_404(id) #Search for the recipe with the id entered; if it doesn't exist, return a 404 error

        return recipe

    @recipe_ns.marshal_with(recipe_model)
    def put(self, id):
        """Update a recipe by id"""
        recipe_update = Recipe.query.get_or_404(id)

        data = request.get_json() #Getting data from the user

        title = data.get("title")
        description = data.get("description")
        if title:
            recipe_update.title_update(title)
        if description:
            recipe_update.des_update(description)

        return recipe_update

    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, id):
        """Delete a recipe by id"""
        recipe_delete = Recipe.query.get_or_404(id)

        recipe_delete.delete()
        return recipe_delete