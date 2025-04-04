recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients seperated by commas: ").split(",")
    ingredients = [item.strip() for item in ingredients]

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe 

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    print("\nRecipe #" + str(i + 1))
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

for recipe in recipes_list:
    name = recipe["name"]
    cooking_time = recipe["cooking_time"]
    ingredients = recipe["ingredients"]
    num_ingredients = len(ingredients)

    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"



    print("\nRecipe:", name)
    print("Cooking Time (min):", cooking_time)
    print("Ingredients:")
    for item in ingredients:
        print(item)
    print("Difficulty level:", difficulty)

def all_ingredients():
    print("Ingredients Available Across All Recipes")
    print("________________________________________")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()