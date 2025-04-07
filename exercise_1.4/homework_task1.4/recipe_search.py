import pickle

def display_recipe(recipe):
    print("\nRecipe Found:")
    print("Name:", recipe["name"])
    print("Cooking Time:", recipe["cooking_time"], "minutes")
    print("Ingredients:", ", ".join(recipe["ingredients"]))
    print("Difficulty:", recipe["difficulty"])

def search_ingredient(data):
    ingredients = data["all_ingredients"]

    if not ingredients:
        print("No ingredients found in data.")
        return

    print("\nAvailable Ingredients:")
    for index, ingredient in enumerate(ingredients):
        print(f"{index}: {ingredient}")

    try:
        choice = int(input("Pick an ingredient by number: "))
        ingredient_searched = ingredients[choice]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number from the list.")
        return
    else:
        print(f"\nSearching for recipes with '{ingredient_searched}'...\n")
        found = False
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)
                found = True
        if not found:
            print("No recipes found with that ingredient.")

filename = input("Enter the recipe file name to search from (e.g., recipes.bin): ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please run recipe_input.py first.")
except:
    print("An unexpected error occurred.")
else:
    search_ingredient(data)
