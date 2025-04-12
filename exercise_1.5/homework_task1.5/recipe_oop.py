class Recipe:
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.calculate_difficulty()

    def get_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    def add_ingredients(self, ingredients):  # Expecting a list
        for ingredient in ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
        self.update_all_ingredients()
        self.calculate_difficulty()

    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def update_all_ingredients(self):
        for item in self.ingredients:
            if item not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(item)

    def __str__(self):
        output = f"\nRecipe: {self.name}\n" \
                 f"Cooking Time (min): {self.cooking_time}\n" \
                 f"Ingredients: {', '.join(self.ingredients)}\n" \
                 f"Difficulty: {self.get_difficulty()}"
        return output


# Simple recipe search function (not inside class)
def recipe_search(data, search_term):
    print(f"\nSearching for recipes with: {search_term}")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


#Main Script

tea = Recipe("Tea")
tea.add_ingredients(["Tea Leaves", "Sugar", "Water"])
tea.set_cooking_time(5)

coffee = Recipe("Coffee")
coffee.add_ingredients(["Coffee Powder", "Sugar", "Water"])
coffee.set_cooking_time(5)

cake = Recipe("Cake")
cake.add_ingredients(["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"])
cake.set_cooking_time(50)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients(["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"])
banana_smoothie.set_cooking_time(5)

# Print all recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

print("\n--- Recipe Book ---")
for recipe in recipes_list:
    print(recipe)

# Search for ingredients
for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)
