import os
import requests
import json

GEMINI_API_KEY = os.getenv("API_KEY")


def generate_recipe(physical_target, ingredient_string, calorie_limit, carbs, fats, protein, meals):
    endpoint_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    meal_sections = ""
    total_meals = 3 * meals

    for i in range(1, total_meals + 1):
        meal_sections += (
            f"  {{\n"
            f'    "name": "Título de la receta ",\n'
            f'    "ingredientMeals": [\n'
            f'      {{"id": "ID del ingrediente 1", "name": "Nombre del ingrediente 1", "grams": Cantidad en gramos}},\n'
            f'      {{"id": "ID del ingrediente 2", "name": "Nombre del ingrediente 2", "grams": Cantidad en gramos}},\n'
            f'      ...\n'
            f'    ],\n'
            f'    "calories": calorías totales de la receta,\n'
            f'    "carbs": Gramos totales de carbohidratos,\n'
            f'    "fats": Gramos totales de grasas,\n'
            f'    "proteins": Gramos totales de proteínas,\n'
            f'    "description": "Instrucciones para preparar la receta {i}."\n'    
            f"  }},\n"
        )

    if meal_sections.endswith(",\n"):
        meal_sections = meal_sections[:-2] + "\n"
    
    prompt_text = (
        f"Usa los siguientes ingredientes: {ingredient_string} para seleccionar los que se incluirán en {total_meals} recetas diferentes. "
        f"Cada receta debe tener un máximo de {calorie_limit} calorías. "
        f"La receta debe estar enfocada en {physical_target}. "
        f"Ten en cuenta la cantidad de: carbohidratos: {carbs} gramos, grasas: {fats} gramos y proteína: {protein} gramos al momento de generar las opciones.\n\n"
        
        f"Devuelve la respuesta estrictamente en el siguiente formato JSON, sin caracteres de escape o información adicional:\n\n"
        f"[\n{meal_sections}\n]"
        
        f"\n\nAsegúrate de que:\n"
        f"- Sólo utilices la información de los ingredientes dados; no incluyas ni generes información de ingredientes nuevos para la receta.\n"
        f"Entrega únicamente este JSON, sin caracteres de escape ni texto adicional."
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }

    response = requests.post(endpoint_url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            raw_json_text = result['candidates'][0]['content']['parts'][0]['text'][7:][:-4]
            
            recipes_list = json.loads(raw_json_text)
            
            return recipes_list
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error al procesar la respuesta: {e}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


