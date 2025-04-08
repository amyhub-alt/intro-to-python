class ShoppingList:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f"'{item}' added to the list.")
        else:
            print(f"'{item}' is already in that list.")


    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f"'{item}' removed from list.")
        else:
             print(f"'{item}' is not in list.")

   
    def view_list(self):
        print(f"\n{self.list_name}:")
        if not self.shopping_list:
            print("The list is empty.")
        else:
            for i, item in enumerate(self.shopping_list, start=1):
                print(f"{i}. {item}")


pet_store_list = ShoppingList("Pet Store Shopping List")

pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("toy")
pet_store_list.add_item("collars")

pet_store_list.remove_item("dog food")

pet_store_list.add_item("toy")

pet_store_list.view_list()