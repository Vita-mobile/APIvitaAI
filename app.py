from flask import Flask, jsonify
from services import get_collection, get_available_and_restrictive_ingredients
from services import generate_ingredient_string
from services import generate_recipe

app = Flask(__name__)

@app.route('/generate-recipes/<user_id>/<int:meals>', methods=['GET'])
def generate_recipes(user_id, meals):
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
