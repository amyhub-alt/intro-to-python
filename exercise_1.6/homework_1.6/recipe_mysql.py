import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Recipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)
''')


# MAIN MENU LOOP 
def main_menu(conn, cursor):
    choice = ''
    
    while choice != 'quit':
        print("\nMain Menu")
        print("=" * 25)
        print("Pick a choice:")
        print("  1. Create a new recipe")
        print("  2. Search for a recipe by ingredient")
        print("  3. Update an existing recipe")
        print("  4. Delete a recipe")
        print("  Type 'quit' to exit the program.")
        
        choice = input("Your choice: ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == 'quit':
            print("Exiting and saving changes.")
            conn.commit()
            conn.close()
        else:
            print("Invalid choice. Please pick 1–4 or type 'quit'.")


def create_recipe(conn, cursor):
    print("\n-- Create a New Recipe --")
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter ingredients (comma-separated): ").split(',')

    ingredients = [ingredient.strip() for ingredient in ingredients]

    def calculate_difficulty(cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            return "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            return "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            return "Intermediate"
        else:
            return "Hard"

    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)

    cursor.execute('''
        INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
        VALUES (%s, %s, %s, %s)
    ''', (name, ingredients_str, cooking_time, difficulty))

    conn.commit()
    print(f"'{name}' added successfully.")


def search_recipe(conn, cursor):
    print("\n-- Search Recipe by Ingredient --")

    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = []

    for row in results:
        ingredients = row[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    for idx, ingredient in enumerate(all_ingredients):
        print(f"{idx + 1}. {ingredient}")

    selected = int(input("Select an ingredient by number: "))
    search_ingredient = all_ingredients[selected - 1]

    cursor.execute(
        "SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s",
        ("%" + search_ingredient + "%",)
    )
    results = cursor.fetchall()

    print(f"\nRecipes containing '{search_ingredient}':")
    for row in results:
        print(row)


def update_recipe(conn, cursor):
    print("\n-- Update an Existing Recipe --")

    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    for recipe in recipes:
        print(f"{recipe[0]}. {recipe[1]}")

    recipe_id = int(input("Enter the ID of the recipe to update: "))

    print("What would you like to update?")
    print("1. Name")
    print("2. Cooking Time")
    print("3. Ingredients")

    update_choice = input("Enter choice (1-3): ")

    if update_choice == '1':
        new_name = input("Enter the new name: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, recipe_id))

    elif update_choice == '2':
        new_time = int(input("Enter the new cooking time: "))
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_time, recipe_id))

        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ingredients_str = cursor.fetchone()[0]
        ingredients = ingredients_str.split(", ")

        def calculate_difficulty(cooking_time, ingredients):
            if cooking_time < 10 and len(ingredients) < 4:
                return "Easy"
            elif cooking_time < 10 and len(ingredients) >= 4:
                return "Medium"
            elif cooking_time >= 10 and len(ingredients) < 4:
                return "Intermediate"
            else:
                return "Hard"

        difficulty = calculate_difficulty(new_time, ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))

    elif update_choice == '3':
        new_ingredients = input("Enter the new ingredients (comma-separated): ").split(',')
        new_ingredients = [i.strip() for i in new_ingredients]
        new_ingredients_str = ", ".join(new_ingredients)

        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]

        def calculate_difficulty(cooking_time, ingredients):
            if cooking_time < 10 and len(ingredients) < 4:
                return "Easy"
            elif cooking_time < 10 and len(ingredients) >= 4:
                return "Medium"
            elif cooking_time >= 10 and len(ingredients) < 4:
                return "Intermediate"
            else:
                return "Hard"

        difficulty = calculate_difficulty(cooking_time, new_ingredients)

        cursor.execute("UPDATE Recipes SET ingredients = %s, difficulty = %s WHERE id = %s",
                       (new_ingredients_str, difficulty, recipe_id))

    conn.commit()
    print("Recipe updated successfully.")


def delete_recipe(conn, cursor):
    print("\n-- Delete a Recipe --")

    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    for recipe in recipes:
        print(f"{recipe[0]}. {recipe[1]}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()

    print("Recipe deleted.")

main_menu(conn, cursor)


