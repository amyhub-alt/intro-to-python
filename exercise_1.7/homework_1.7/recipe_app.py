from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

Base = declarative_base()

class Recipe(Base):
    __tablename__="final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name} ({self.difficulty})>"

    def __str__(self):
        return (
            f"\nRecipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time (min): {self.cooking_time}\n"
            f"Difficulty: {self.difficulty}\n"
            + "-" * 30
        )

    def calculate_difficulty(self):
        ingredients_list = self.return_ingredients_as_list()
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients_list) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients_list) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return [ingredient.strip() for ingredient in self.ingredients.split(",")]

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_recipe():
    name = input("Enter the recipe name: ")
    while len(name) > 50:
        print("Name is too long. Please enter a name with 50 characters or fewer.")
        name = input("Enter the recipe name: ")

    try:
        cooking_time = int(input("Enter the cooking time in minutes: "))
    except ValueError:
        print("Invalid input. Cooking time must be a number.")
        return

    try:
        num_ingredients = int(input("How many ingredients would you like to enter? "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    ingredients = []
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)

    ingredients_str = ", ".join(ingredients)

    new_recipe = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )
    new_recipe.calculate_difficulty()
    session.add(new_recipe)
    session.commit()
    print("Recipe added successfully!")

def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found in the database.")
        return
    for recipe in recipes:
        print(recipe)


def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return

    results = session.query(Recipe.ingredients).all()
    all_ingredients = set()
    for result in results:
        ingredients = result[0].split(", ")
        all_ingredients.update(ingredients)

    all_ingredients = list(all_ingredients)
    for idx, ingredient in enumerate(all_ingredients, 1):
        print(f"{idx}. {ingredient}")

    selected_numbers = input("Enter the numbers of the ingredients you want to search for, separated by spaces: ")
    try:
        selected_indices = [int(num) - 1 for num in selected_numbers.split()]
        search_ingredients = [all_ingredients[i] for i in selected_indices]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]
    recipes = session.query(Recipe).filter(*conditions).all()

    if not recipes:
        print("No recipes found with the selected ingredients.")
        return

    for recipe in recipes:
        print(recipe)


def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("No recipes found in the database.")
        return

    for recipe in recipes:
        print(f"{recipe.id}. {recipe.name}")

    try:
        recipe_id = int(input("Enter the ID of the recipe you want to edit: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    recipe_to_edit = session.query(Recipe).get(recipe_id)
    if not recipe_to_edit:
        print("Recipe not found.")
        return

    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time}")

    choice = input("Enter the number of the attribute you want to edit: ")
    if choice == "1":
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif choice == "2":
        new_ingredients = input("Enter the new ingredients (separated by commas): ")
        recipe_to_edit.ingredients = new_ingredients
    elif choice == "3":
        try:
            new_cooking_time = int(input("Enter the new cooking time: "))
            recipe_to_edit.cooking_time = new_cooking_time
        except ValueError:
            print("Invalid input. Cooking time must be a number.")
            return
    else:
        print("Invalid choice.")
        return

    recipe_to_edit.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")


def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("No recipes found in the database.")
        return

    for recipe in recipes:
        print(f"{recipe.id}. {recipe.name}")

    try:
        recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    recipe_to_delete = session.query(Recipe).get(recipe_id)
    if not recipe_to_delete:
        print("Recipe not found.")
        return

    confirm = input(f"Are you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ").lower()
    if confirm == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Deletion cancelled.")


def main():
    while True:
        print("\nRecipe App Main Menu")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit the application.")
        
        choice = input("Enter your choice: ").lower()
        
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("Goodbye!")
            session.close()
            engine.dispose()
            break
        else:
            print("Invalid input. Please choose a valid option.")


if __name__ == "__main__":
    main()
