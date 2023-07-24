# from flask import Flask, jsonify, request
# from http import HTTPStatus

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello'

# recipes = [
#     {
#         'id':1,
#         'name':'Egg Salad',
#         'description':'This is lovely egg salad recipe'
#     },
#     {
#         'id':2,
#         'name':'Tomato Pasta',
#         'description':'This is lovely tomato pasta recipe'
#     }
# ]

# @app.route('/recipes/', methods=['GET'])
# def get_recipes():
#     return jsonify({'data':recipes})


# @app.route('/recipes/<int:recipe_id>', methods=['GET'])
# def get_recope(recipe_id):
#     recipe = next((recipe for recipe in recipes if recipe['id']==recipe_id), None)
#     if recipe:
#         return jsonify(recipe)
#     return jsonify({'message':'recipe not found'}), 404

# @app.route('/recipes', methods=['POST'])
# def create_recipe():
#     data = request.get_json()
#     name = data.get('name')
#     description = data.get('description')
#     recipe = {
#         'id':len(recipes)+1,
#         'name':name,
#         'description':description
#     }
#     recipes.append(recipe)
#     return jsonify(recipe), 201

# @app.route('/recipes/<int:recipe_id>',methods=['PUT'])
# def update_recipe(recipe_id):
#     recipe = next((recipe for recipe in recipes if recipe['id']==recipe_id),None)
#     if not recipe:
#         return jsonify({'message':'resipe not found'}), 404
#     data = request.get_json()
#     recipe.update(
#         {
#             'name':data.get('name'),
#             'description':data.get('description')
#         }
#     )    
#     return jsonify(recipe)

# if __name__=='__main__':
#     app.run()

# a = [int(i) for i in input().split()]
# print(a)
# import os
# from dotenv import load_dotenv
# load_dotenv()
# print(os.environ.get('MAILGUN_API_KEY'))