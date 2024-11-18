from flask import Flask, jsonify, request
from services import get_collection, get_available_and_restrictive_ingredients
from services import generate_ingredient_string
from services import generate_recipe
import firebase_admin
from firebase_admin import credentials, auth
import os 
import json
from services.firebase_config import get_db
    

app = Flask(__name__)


def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return "Error on authentication: " + str(e)


@app.route('/generate-recipes/<user_id>/<int:meals>', methods=['GET'])
def generate_recipes(user_id, meals):
    
    
    #Auth process
    
    
    id_token = request.headers.get('Authorization')
    
    if id_token is None:
        
        return jsonify({"error": "Token de autenticación no proporcionado"}), 401
    
    id_token= id_token.split("Bearer ")[1]
    
    decoded_token = verify_token(id_token)
    
    print("Decoded token has: ", decoded_token)
    
    if decoded_token is None:
        return jsonify({"error": "Token de autenticación inválido"}), 403
    
    try:
        physical_target, preferences, restrictions, calorie_limit, carbs, fats, protein = get_available_and_restrictive_ingredients(user_id)
        ingredients = get_collection("Ingredient")

        ingredient_string = generate_ingredient_string(ingredients, preferences, restrictions)

        recipes = generate_recipe(physical_target, ingredient_string, calorie_limit, carbs, fats, protein, meals)

        return jsonify(recipes)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
