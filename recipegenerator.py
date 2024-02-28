from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

def add_recipe():

    # Create the 'Recipes' table if it doesn't exist
    con2 = sqlite3.connect("recipes.db")
    cursor = con2.cursor()
    cursor.execute ('''CREATE TABLE IF NOT EXISTS Recipes (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        RecipeName TEXT,
                        Ingredients TEXT,
                        Instructions TEXT
                        )''')
    con2.commit()
    con2.close()

    def add_recipe_to_db():
        # Fetch data from widgets
        recipe_name = recipe_name_text.get("1.0", "end-1c")
        ingredients = ingredients_text.get("1.0", "end-1c")
        instructions = instructions_text.get("1.0", "end-1c")
        
        # Store data in the database
        con2 = sqlite3.connect("recipes.db")  # Update with your existing database name
        cursor = con2.cursor()
        cursor.execute("INSERT INTO Recipes (RecipeName, Ingredients, Instructions) VALUES (?, ?, ?)", (recipe_name, ingredients, instructions))
        con2.commit()
        con2.close()

        # Open a new window to prompt user's action
        add_another_window = Toplevel(root)
        add_another_window.title("Recipe Added")
        add_another_window.geometry("600x400+340+160")

        # Label to prompt user
        prompt_label = Label(add_another_window, text="Recipe added successfully!\nDo you want to add another recipe or view added recipes?")
        prompt_label.pack()

        # Buttons to add another recipe or view added recipes
        add_another_button = Button(add_another_window, text="Add Another Recipe", command=add_recipe)
        add_another_button.place(x=200,y=50)

        view_recipes_button = Button(add_another_window, text="View Added Recipes", command=view_recipes)
        view_recipes_button.place(x=200,y=80)
       
    def view_recipes():
        # Fetch recipes from the database and display them in a new window
        con2 = sqlite3.connect("recipes.db")
        cursor = con2.cursor()
        cursor.execute("SELECT * FROM Recipes")
        recipes = cursor.fetchall()
        con2.close()

        # Open a new window to display added recipes
        view_recipes_window = Toplevel(root)
        view_recipes_window.title("View Added Recipes")
        view_recipes_window.geometry("1080x1080+340+160")

        # Create Treeview widget
        tree = ttk.Treeview(view_recipes_window)
        tree["columns"] = ("Recipe Name", "Ingredients", "Instructions")
        tree.column("#0", width=0, stretch=NO)  # Hide the first column
        tree.column("Recipe Name", width=200, anchor=W)
        tree.column("Ingredients", width=300, anchor=W)
        tree.column("Instructions", width=300, anchor=W)

        tree.heading("Recipe Name", text="Recipe Name")
        tree.heading("Ingredients", text="Ingredients")
        tree.heading("Instructions", text="Instructions")

        # Insert data into Treeview
        for recipe in recipes:
            tree.insert("", END, values=(recipe[1], recipe[2], recipe[3]))

        tree.pack(expand=True, fill=BOTH)

        # Button to close the window
        close_button = Button(view_recipes_window, text="Close", command=view_recipes_window.destroy)
        close_button.pack()

        # Update ingredient list in find_recipe function if necessary

    new_window = Toplevel(root)
    new_window.title("Add Recipe")
    new_window.geometry("600x400+340+160")

    

    # Your other GUI elements here
    recipe_name_label = Label(new_window, text="Enter Recipe Name:")
    recipe_name_label.place(x=95 , y=50)

    recipe_name_text = Text(new_window, width=15, height=1)
    recipe_name_text.place(x=205, y=50)

    # Your other GUI elements here
    ingredients_label = Label(new_window, text="Enter Ingredients:")
    ingredients_label.place(x=100, y=90)

    ingredients_text = Text(new_window, width=15, height=1)
    ingredients_text.place(x=205, y=90)

    # Your other GUI elements here
    instructions_label = Label(new_window, text="Enter Instructions:")
    instructions_label.place(x=100, y=130)

    instructions_text = Text(new_window, width=15, height=1)
    instructions_text.place(x=205, y=130)

    # Submit Button
    browse_button = Button(new_window, text="Submit", command = add_recipe_to_db)
    browse_button.place(x=205,y=180)
    
    home_button = Button(new_window, text="Home", command = new_window.destroy)
    home_button.place(x=0,y=0)

def find_recipe():
    new_window = Toplevel(root)

    # Create a database connection
    conn = sqlite3.connect("ingredients_recipe.db")

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Function to update the ingredient list
    def add_ingredient():
        ingredient_listbox.delete(0, END)
        for ingredient in receipes:
            ingredient_listbox.insert(END, ingredient)

    new_window.title("Find Recipe")
    new_window.geometry("600x400+340+160")
    
    home_button = Button(new_window, text="Home", command = new_window.destroy)
    home_button.place(x = 10, y = 10)

    # Your other GUI elements here
    label = Label(new_window, text="Search Here :")
    label.place(x=115 , y=50)

    # Ingredient Entry
    ingredient_label = Label(new_window, text="(Enter an Ingredient / Recipe name)")
    ingredient_label.place(x=80,y=80)

    # Create a Text widget to display file contents
    text_widget = Text(new_window , width=15, height=1)
    text_widget.place(x=205,y=50)
       
    # Buttons
    generate_button = Button(new_window, text="Generate Recipe", command = fetch_recipe)
    generate_button.place(x=205, y=125)

    root.mainloop()

def fetch_recipe():

    generated_pages = []

    # Your logic to generate recipe content
    recipe_content = "This is a generated recipe."

    # Create a new page for displaying generated content
    generated_page = Toplevel(root)
    generated_page.geometry('600x400+340+160')


    # Configure GUI elements on the generated page
    recipe_label = Label(generated_page, text=f"Generated Recipe:\n{recipe_content}")
    recipe_label.pack()

    ingredient_list_label = Label(generated_page, text="Recipes:")
    ingredient_list_label.place(x=235,y=35)
    ingredient_listbox = Listbox(generated_page)
    ingredient_listbox.place(x=235,y=70)

    # Button to go back to the main page
    back_to_main_button = Button(generated_page, text="Back to Main Page", command=generated_page.destroy)
    back_to_main_button.place(x=10,y=10)

    # Set the current page to the generated page
    generated_pages.append(generated_page)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Random Recipe Generator")
        self.master.geometry("600x400+340+160")
        self.create_widgets()

    def create_widgets(self):
        self.bg_image = self.load_image("logo.png", (650, 400))
        self.bg_label = Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.heading_label = Label(self.master, text="Random Recipe Generator", font=("Times New Roman", 20, "bold"), bg="white")
        self.heading_label.place(x=250, y=0)

        self.add_button = Button(self.master, text="Add a Recipe", command=self.add_recipe)
        self.add_button.place(x=450, y=100)

        self.find_button = Button(self.master, text="Find a Recipe", command=self.find_recipe)
        self.find_button.place(x=450, y=160)

    def load_image(self, path, size):
        bg_image = Image.open(path)
        bg_image = bg_image.resize(size)
        return ImageTk.PhotoImage(bg_image)

    def add_recipe(self):
        add_recipe_window = Toplevel(self.master)
        add_recipe_window.title("Add Recipe")
        add_recipe_window.geometry("600x400+340+160")
        self.add_bg_image(add_recipe_window)

        # Your add_recipe GUI elements here

    def find_recipe(self):
        find_recipe_window = Toplevel(self.master)
        find_recipe_window.title("Find Recipe")
        find_recipe_window.geometry("600x400+340+160")
        self.add_bg_image(find_recipe_window)

        # Your find_recipe GUI elements here

    def add_bg_image(self, window):
        bg_label = Label(window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()

    # Add buttons
    add_button = Button(root, text="Add a Recipe", command = add_recipe)
    add_button.place(x=450,y=100)

    find_button = Button(root, text="Find a Recipe", command = find_recipe)
    find_button.place(x=450,y=160)

if __name__ == "__main__":
    main()