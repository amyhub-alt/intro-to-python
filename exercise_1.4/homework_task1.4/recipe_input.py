import pickle

def take_recipe():
    name = input('Enter name of the recipe: ')
    cooking_time = int(input('Enter the cooking time in minutes: '))
    ingredients = input('Enter the ingredients separated by commas: ').split(',')
    ingredients = [item.strip() for item in ingredients]  # Fixed typo here
    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    return recipe

def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    return difficulty

filename = input("Enter the name of the file you want to save to: ")

try:
    with open(filename, 'rb') as file:  # Use filename (not 'filename' string)
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Creating new recipe data.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
except:
    print("Something went wrong. Creating new recipe data.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    print("File loaded successfully!")
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

num_recipes = int(input("How many recipes would you like to enter? "))

for _ in range(num_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for item in recipe["ingredients"]:
        if item not in all_ingredients:
            all_ingredients.append(item)

data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

with open(filename, 'wb') as file:
    pickle.dump(data, file)

print(f"\nRecipes saved to {filename}!")
