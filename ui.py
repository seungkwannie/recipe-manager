import tkinter as tk
from tkinter import messagebox, ttk
from manager import RecipeManager


class RecipeManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Manager")
        self.root.geometry("600x700")

        self.manager = RecipeManager()
        self.editing_id = None  # Tracks if we are editing or adding

        # UI Elements
        self.setup_ui()
        self.refresh_recipe_list()

    def setup_ui(self):
        # 1. Input Form (The 'recipe_form' in your Rust code)
        form_frame = ttk.LabelFrame(self.root, text="Recipe Details", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        self.name_var = tk.StringVar()
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky="ew")

        self.ingredients_var = tk.StringVar()
        ttk.Label(form_frame, text="Ingredients (comma-separated):").grid(row=1, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.ingredients_var).grid(row=1, column=1, sticky="ew")

        self.instructions_var = tk.StringVar()
        ttk.Label(form_frame, text="Instructions (line-separated):").grid(row=2, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.instructions_var).grid(row=2, column=1, sticky="ew")

        self.servings_var = tk.StringVar()
        ttk.Label(form_frame, text="Servings:").grid(row=3, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.servings_var).grid(row=3, column=1, sticky="ew")

        self.action_btn = ttk.Button(form_frame, text="Add Recipe", command=self.handle_action)
        self.action_btn.grid(row=4, column=1, sticky="e", pady=5)

        # 2. Recipe List (The 'Scrollable' list in Rust)
        list_frame = ttk.LabelFrame(self.root, text="Your Recipes", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(list_frame)
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_content = ttk.Frame(self.canvas)

        self.scroll_content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 3. Bottom Controls (Save/Load)
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Save Recipes", command=self.save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Load Recipes", command=self.load).pack(side="left", padx=5)

    def handle_action(self):
        name = self.name_var.get()
        ing = self.ingredients_var.get().split(",")
        ins = self.instructions_var.get().split("\n")
        try:
            srv = int(self.servings_var.get())
        except ValueError:
            srv = 1

        if self.editing_id is None:
            self.manager.add_recipe(name, ing, ins, srv)
        else:
            self.manager.update_recipe(self.editing_id, name, ing, ins, srv)
            self.editing_id = None
            self.action_btn.config(text="Add Recipe")

        self.clear_form()
        self.refresh_recipe_list()

    def refresh_recipe_list(self):
        # Clear existing widgets in the list
        for widget in self.scroll_content.winfo_children():
            widget.destroy()

        for recipe in self.manager.get_all_recipes():
            row = ttk.Frame(self.scroll_content)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=recipe.name, width=20).pack(side="left")
            ttk.Button(row, text="Edit", command=lambda r=recipe: self.edit_recipe(r)).pack(side="left", padx=2)
            ttk.Button(row, text="Delete", command=lambda r=recipe: self.delete_recipe(r.id)).pack(side="left")

    def edit_recipe(self, recipe):
        self.name_var.set(recipe.name)
        self.ingredients_var.set(",".join(recipe.ingredients))
        self.instructions_var.set("\n".join(recipe.instructions))
        self.servings_var.set(str(recipe.servings))
        self.editing_id = recipe.id
        self.action_btn.config(text="Update Recipe")

    def delete_recipe(self, rid):
        if self.manager.delete_recipe(rid):
            self.refresh_recipe_list()

    def save(self):
        self.manager.save_to_file("recipes.json")
        messagebox.showinfo("Success", "Recipes saved!")

    def load(self):
        self.manager.load_from_file("recipes.json")
        self.refresh_recipe_list()

    def clear_form(self):
        self.name_var.set("")
        self.ingredients_var.set("")
        self.instructions_var.set("")
        self.servings_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeManagerGUI(root)
    root.mainloop()