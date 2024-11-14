def generate_ingredient_string(ingredients, preferences, restrictions):
    
    print("INGREDIENTES: ", ingredients)
    
    print("PREFERENCIAS: ", preferences)
    
    print("RESTRICCIONES: ", restrictions)
    
    result_string = "Alimentos principales:/n"
    
    for ingredient in ingredients:
        if any(pref["id"] == ingredient["id"] for pref in preferences):
            result_string += (f"- {ingredient['name']} (ID: {ingredient['id']}): "
                              f"{ingredient['calories']} kcal, {ingredient['protein']} g de proteína, "
                              f"{ingredient['carbs']} g de carbohidratos, {ingredient['fats']} g de grasas./n")
    
    result_string += "/nAlimentos secundarios:/n"
    
    for ingredient in ingredients:
        if not any(pref["id"] == ingredient["id"] for pref in preferences) and \
           not any(restr["id"] == ingredient["id"] for restr in restrictions):
            result_string += (f"- {ingredient['name']} (ID: {ingredient['id']}): "
                              f"{ingredient['calories']} kcal, {ingredient['protein']} g de proteína, "
                              f"{ingredient['carbs']} g de carbohidratos, {ingredient['fats']} g de grasas./n")
    
    return result_string