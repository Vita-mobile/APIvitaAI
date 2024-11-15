import firebase_admin
from firebase_admin import credentials, firestore
import os
import json


firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')

if not firebase_credentials:
    raise ValueError("Enviroment variable FIREBASE_CREDENTIALS is not set.")

credentials_json = json.loads(firebase_credentials)

cred = credentials.Certificate(credentials_json)    

firebase_admin.initialize_app(cred)

db = firestore.client()

def get_collection(collection_name):
    ingredients = list()
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    
    for doc in docs:
        ingredients.append(doc.to_dict())
    return ingredients

def get_available_and_restrictive_ingredients(user_id):
    user_ref = db.collection("User").document(user_id)
    user_doc = user_ref.get()
    
    if not user_doc.exists:
        print(f"El usuario con id {user_id} no existe.")
        return None
    
    user_data = user_doc.to_dict()
    physical_target = user_data.get("physicalTarget")

    nutritional_plan_ref = user_ref.collection("NutritionalPlan").limit(1)
    nutritional_plan_docs = nutritional_plan_ref.stream()
    nutritional_plan_doc = next(nutritional_plan_docs, None)
    
    if nutritional_plan_doc is None or not nutritional_plan_doc.exists:
        print(f"El plan nutricional no existe para el usuario con id {user_id}.")
        return None

    nutritional_plan_data = nutritional_plan_doc.to_dict()
    restrictions = nutritional_plan_data.get("restrictions")
    preferences = nutritional_plan_data.get("preferences")
    carbs = nutritional_plan_data.get("carbs", 0)
    fats = nutritional_plan_data.get("fats", 0)
    protein = nutritional_plan_data.get("protein", 0)
    goal = nutritional_plan_data.get("kcalGoal", 0)
    meals = nutritional_plan_data.get("meals", 1)
    
    if meals == 0:
        print("El número de comidas no puede ser cero.")
        return None
    
    return physical_target, preferences, restrictions, goal/meals, carbs/meals, fats/meals, protein/meals
