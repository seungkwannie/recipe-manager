import json
from typing import List, Optional
from recipe import Recipe

class RecipeManager:
    def __init__(self):
        self.recipes: List[Recipe] = []
        self.next_id: int = 1

    def add_recipe(self, name: str, ingredients: List[str], instructions: List[str], servings: int) -> int:
        recipe_id = self.next_id
        new_recipe = Recipe(recipe_id, name, ingredients, instructions, servings)
        self.recipes.append(new_recipe)
        self.next_id += 1
        return recipe_id

    def get_all_recipes(self) -> List[Recipe]:
        return self.recipes

    def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        # Equivalent to Rust's .find()
        return next((r for r in self.recipes if r.id == recipe_id), None)

    def update_recipe(self, recipe_id: int, name: str, ingredients: List[str], instructions: List[str], servings: int) -> bool:
        recipe = self.get_recipe(recipe_id)
        if recipe:
            recipe.name = name
            recipe.ingredients = ingredients
            recipe.instructions = instructions
            recipe.servings = servings
            return True
        return False

    def delete_recipe(self, recipe_id: int) -> bool:
        initial_len = len(self.recipes)
        # Replaces Rust's .retain()
        self.recipes = [r for r in self.recipes if r.id != recipe_id]
        return len(self.recipes) < initial_len

    def save_to_file(self, filename: str):
        # Converts list of objects into a list of dictionaries for JSON
        with open(filename, 'w') as f:
            data = [vars(r) for r in self.recipes]
            json.dump(data, f)

    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                # Reconstruct Recipe objects from the JSON data
                self.recipes = [Recipe(**d) for d in data]
                # Update next_id based on highest existing ID
                if self.recipes:
                    self.next_id = max(r.id for r in self.recipes) + 1
        except FileNotFoundError:
            print("No save file found. Starting fresh.")