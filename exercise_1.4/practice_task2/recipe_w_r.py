import pickle

recipe = {
    'name': 'Tea',
    'ingredients': ['Tea leaves', 'Water', 'Sugar'],
    'cooking_time': 5, 
    'difficulty': 'Easy'
}

with open('recipe_binary.bin', 'wb') as my_file:
    pickle.dump(recipe, my_file)

with open('recipe_binary.bin', 'rb') as my_file:
    loaded_recipe = pickle.load(my_file)


print("Recipe Details:")
print(f"Name: {loaded_recipe['name']}")
print(f"Ingredients: {', '.join(loaded_recipe['ingredients'])}")
print(f"Cooking Time: {loaded_recipe['cooking_time']} minutes")
print(f"Difficulty: {loaded_recipe['difficulty']}")