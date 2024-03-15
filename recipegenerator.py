from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox, ttk, Menu
import re

def create_home_button(parent_window, main_window):
    # Load and resize the image
    image = Image.open("login_page_img.png")
    image = image.resize((20, 20))

    # Convert the image to a PhotoImage object
    photo = ImageTk.PhotoImage(image)

    # Adding icon
    icon_image = PhotoImage(file="login_page_img.png")
    main_window.iconphoto(True, icon_image)

    # Create a button with the image
    button = Button(parent_window, image=photo, command=lambda: go_to_home(parent_window, main_window))
    button.pack()

def go_to_home(parent_window, main_window):
    # Destroy current window
    parent_window.destroy()

    # Recreate the home page window
    main_window.deiconify()  # Restore main window if minimized

class SignupPage:
    def __init__ (self, master):
        self.master = master
        master.title("Signup Page")
        master.geometry("900x550+0+0")  # Set the dimensions to 900x550
        master.resizable(False, False)  # Disable window resizing

        # Create the table if not exists
        self.create_table()

        # Load and resize the background image
        bg_image = Image.open("login_page_img.png")
        bg_image = bg_image.resize((900, 550))
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(bg_image)

        # Adding icon
        icon_image = PhotoImage(file="login_page_img.png")
        master.iconphoto(True, icon_image)
        master.iconbitmap(r"logo.png")

        # Create a label to display the background image
        bg_label = Label(master, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading
        heading_label = Label(master, text="RECIPE GENERATOR\n\nSign up", font=("Times New Roman", 20, "bold"),bg="white",fg="red")
        heading_label.place(x=500, y=80)

        #email label and entry
        self.email_label = Label(master, text="Email:",font=("Times New Roman", 16,"bold"), bg="white", fg="orangered")
        self.email_label.place(relx=0.58, rely=0.45, anchor=CENTER)
        self.email_entry = Entry(master, width=35, font=("Times New Roman", 11), highlightbackground="orangered",  highlightcolor="orangered",highlightthickness=2)
        self.email_entry.place(relx=0.8, rely=0.45, anchor=CENTER)


        # Password label and entry
        self.password_label = Label(master, text="Password:",font=("Times New Roman",16,"bold"), bg="white",fg="orangered")
        self.password_label.place(relx=0.6, rely=0.55, anchor=CENTER)
        self.password_entry = Entry(master, show="*", width=35,font=("Times New Roman", 11,),highlightbackground="orangered",  highlightcolor="red",highlightthickness=2)
        self.password_entry.place(relx=0.8, rely=0.55, anchor=CENTER)


        # Signup button
        self.signup_button = Button(master, text="Signup",font=("Times New Roman", 15), bg="yellow", command=self.signup, width=10)
        self.signup_button.place(relx=0.75, rely=0.7, anchor=CENTER)


        # Already a user label
        self.login_label = Label(master, text="Already an existing user?    |", font=("Times New Roman", 13), bg="white")
        self.login_label.place(relx=0.7, rely=0.8, anchor=CENTER)

        # Create a clickable link to login page
        self.login_link = Label(master, text="Login", font=("Times New Roman", 13),bg="white", fg="blue",cursor="hand2")
        self.login_link.place(relx=0.85, rely=0.8, anchor=CENTER)
        self.login_link.bind("<Button-1>", self.show_login)

    def signup(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if the email is valid
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Enter a Valid Email")
            return

        conn = sqlite3.connect('recipe_generator.db')
        c = conn.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM login_details WHERE email=?", (email,))
        user = c.fetchone()

        if user:
            conn.close()
            self.show_user_exists_popup()
        else:
            c.execute("INSERT INTO login_details (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Signup successful! Login into your account")
            self.show_login(None)  # Open the login page after signup

    def is_valid_email(self, email):
        # Regular expression for email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|aol\.com|mail\.com|outlook\.com|protonmail\.com)$'
        return re.match(email_pattern, email) is not None

    def create_table(self):
        conn = sqlite3.connect('recipe_generator.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS login_details(email TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()
        conn.close()

    
    def show_user_exists_popup(self):
        popup = Tk()
        popup.title("User Already Exists")
        popup.geometry("300x100")
        popup.resizable(False, False)

        label = Label(popup, text="The user already exists!", padx=10, pady=10)
        label.pack()

        login_button = Button(popup, text="Login Here", command=lambda: (self.close_popup(popup),self.show_login(popup)))
        login_button.pack()
        
        popup.mainloop()

    def show_login(self, event=None):
        self.master.destroy()  # Close the signup page
        root = Tk()
        app = LoginPage(root)
        root.mainloop()

    def close_popup(self, popup):
        popup.destroy()

class ForgotPasswordPage:
    def _init_(self, master, email):
        self.master = master
        master.title("Reset Password")
        master.geometry("400x200")  # Set the dimensions to 400x200
        master.resizable(False, False)  # Disable window resizing


        self.email = email
        # New Password label and entry
        self.new_password_label = Label(master, text="New Password:")
        self.new_password_label.grid(row=0, column=0, padx=10, pady=10, sticky=E)
        self.new_password_entry = Entry(master, show="*", width=30)
        self.new_password_entry.grid(row=0, column=1, padx=10, pady=10)

        # Confirm Password label and entry
        self.confirm_password_label = Label(master, text="Confirm Password:")
        self.confirm_password_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.confirm_password_entry = Entry(master, show="*", width=30)
        self.confirm_password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Submit button
        self.submit_button = Button(master, text="Submit", command=self.submit, width=10)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def submit(self):
        # Implement the password reset functionality here
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate if passwords match
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            return
        

        #update password in database
        conn = sqlite3.connect('recipe_generator.db')
        c = conn.cursor()
        c.execute("UPDATE login_details SET password = ? WHERE email = ?", (new_password, self.email))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password updated successfully!")
        self.master.destroy()


class LoginPage:
    login_page_instance = None
    def __init__(self, master):
        self.master = master
        master.title("Login Page")
        master.geometry("900x550+0+0")  # Set the dimensions to 900x550
        master.resizable(False, False)  # Disable window resizing
        self.logged_in_user_email = None  # Store the logged-in user's email

        # Load and resize the background image
        bg_image = Image.open("login_page_img.png")
        bg_image = bg_image.resize((900, 550))
        self.bg_image = ImageTk.PhotoImage(bg_image)

        master.iconbitmap(r"logo.png")

        # Create a label to display the background image
        bg_label = Label(master, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #heading label and entry
        heading_label = Label(master, text="RECIPE GENERATOR\n\nLogin", font=("Times New Roman", 20, "bold"),bg="white",fg="brown")
        heading_label.place(x=500, y=80)

        #email label and entry
        self.email_label = Label(master, text="Email:",font=("Times New Roman", 16,"bold"), bg="white", fg="green")
        self.email_label.place(relx=0.58, rely=0.45, anchor=CENTER)
        self.email_entry = Entry(master, width=35, font=("Times New Roman", 11), highlightbackground="green",  highlightcolor="green",highlightthickness=2)
        self.email_entry.place(relx=0.8, rely=0.45, anchor=CENTER)

        
         # Password label and entry
        self.password_label = Label(master, text="Password:",font=("Times New Roman",16,"bold"), bg="white",fg="green")
        self.password_label.place(relx=0.6, rely=0.55, anchor=CENTER)
        self.password_entry = Entry(master, show="*", width=35,font=("Times New Roman", 11,),highlightbackground="green",  highlightcolor="green",highlightthickness=2)
        self.password_entry.place(relx=0.8, rely=0.55, anchor=CENTER)

        # Error label for displaying error messages
        self.error_label = Label(master, text="", fg="red")
        self.error_label.grid(row=2, columnspan=2, pady=5)  # Adjusted row to 2, span across columns

        #Login button
        self.signup_button = Button(master, text="Login",font=("Times New Roman", 15), bg="yellow", command=self.login, width=10)
        self.signup_button.place(relx=0.75, rely=0.7, anchor=CENTER)

        # Forgot password link
        self.forgot_password_label = Label(master, text="Forgot Password?", font=("Times New Roman", 13), fg="blue", cursor="hand2",bg="white")
        self.forgot_password_label.place(relx=0.8, rely=0.6, anchor=CENTER)
        self.forgot_password_label.bind("<Button-1>", self.forgot_password)

        # Don't have an account label
        self.signup_label = Label(master, text="Don't have an account? ", font=("Times New Roman", 10), bg="white")
        self.signup_label.place(relx=0.7, rely=0.8, anchor=CENTER)

        # Create a clickable link to signup page
        self.signup_link = Label(master, text="Signup", font=("Times New Roman", 10, "underline"), fg="blue",cursor="hand2")
        self.signup_link.place(relx=0.8, rely=0.8, anchor=CENTER)
        self.signup_link.bind("<Button-1>", self.show_signup)

        # Store the instance in the class variable
        LoginPage.login_page_instance = self

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if email or password is empty
        if not email or not password:
            self.error_label.config(text="Email or password values cannot be empty.")
            return

        conn = sqlite3.connect('recipe_generator.db')
        c = conn.cursor()
        c.execute("SELECT * FROM login_details WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.logged_in_user_email = email
            self.open_home_page()  # Open homepage upon successful login
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def forgot_password(self, event):
         # Open the forgot password window
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Error", "Please enter your email address.")
            return

        forgot_password_window = Tk()
        forgot_password_page = ForgotPasswordPage(forgot_password_window, email)

    def open_home_page(self):
    
        self.master.destroy()  # Close the login page
        root = self.master  # Use the existing root instance
        app = HomePage(root)

    def show_signup(self, event):
        self.master.destroy()  # Close the login page
        root = Tk()
        app = SignupPage(root)
        root.mainloop()

class HomePage:
    def __init__(self, root):
        # Create main window
        root = Tk()
        root.title("Random Recipe Generator")
        root.resizable(False, False)
        icon_image = PhotoImage(file="login_page_img.png")
        root.iconphoto(True, icon_image)
        root.iconbitmap(r"logo.png")

        # Create a label for displaying error messages
        global error_label
        error_label = Label(root, text="", fg="red")
        error_label.place(x=100, y=210)

        global geometry 
        geometry = "900x550+0+0"
   
        #Heading
        heading_label = Label(root, text="Random Recipe Generator", font=("Times New Roman", 20, "bold"), bg="white")
        heading_label.place(x=510, y=90)

        # Set window dimensions and position
        window_width = 900
        window_height = 550
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        geometry = f"900x550+{(root.winfo_screenwidth() - 900) // 2}+{(root.winfo_screenheight() - 550) // 2}"


        # Add buttons
        add_button = Button(root, text="Add a Recipe", command=add_recipe)
        add_button.place(x=650, y=170)

        find_button = Button(root, text="Find a Recipe", command=find_recipe)
        find_button.place(x=650, y=230)

        # Add Account Button
        account_button = Button(self.root, text="Account", command=self.open_account_menu)
        account_button.place(x=770, y=20)

        def open_account_menu(self):
            # Create a new window for account options
            account_window = Toplevel(self.root)
            account_window.title("Account Options")

            # Account information label
            email_label = Label(account_window, text="Email: example@example.com", font=("Arial", 12))
            email_label.pack()

            # Button to view recipes
            view_recipes_button = Button(account_window, text="View Recipes", command=self.view_recipes)
            view_recipes_button.pack()

        def view_recipes(self):
            # Implement logic to view added recipes here
            print("View Recipes command executed")

        # Run the application
        root.mainloop()

def add_recipe():
    def view_recipes():
        # Retrieve the logged-in user's email from the LoginPage instance
        email = LoginPage.login_page_instance.logged_in_user_email

        # Fetch recipes from the database for the logged-in user's email
        con2 = sqlite3.connect("recipe_generator.db")
        cursor = con2.cursor()
        cursor.execute("SELECT RecipeName, Ingredients, Instructions FROM Recipes WHERE EmailId=?", (email,))
        recipes = cursor.fetchall()
        con2.close()

        # Open a new window to display added recipes
        view_recipes_window = Toplevel(new_window)
        view_recipes_window.title("View Added Recipes")
        view_recipes_window.geometry("900x550+0+0")
        view_recipes_window.resizable(False, False)

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
            tree.insert("", END, values=(recipe[0], recipe[1], recipe[2]))

        tree.pack(expand=True, fill=BOTH)


    def add_recipe_to_db():
        # Fetch data from widgets
        recipe_name = recipe_name_text.get("1.0", "end-1c").strip()
        ingredients = ingredients_text.get("1.0", "end-1c").strip()
        instructions = instructions_text.get("1.0", "end-1c").strip()

        # Retrieve the value of publish_variable
        publish_value = publish_variable.get()

        # Validate input
        if not recipe_name or not ingredients or not instructions:
            error_label.config(text="Please fill in all fields.", fg="red")
            error_label.place(x=405, y=370)
            return
        

        # Retrieve the logged-in user's email from the LoginPage instance
        email = LoginPage.login_page_instance.logged_in_user_email

        try:
            # Store data in the 'Recipes' table
            con2 = sqlite3.connect("recipe_generator.db")
            cursor = con2.cursor()

            # Ensure that email is a string
            if not isinstance(email, str):
                raise ValueError("Email must be a string")

            cursor.execute("INSERT INTO Recipes (EmailId, RecipeName, Ingredients, Instructions) VALUES (?, ?, ?, ?)",
                        (email, recipe_name, ingredients, instructions))
            recipe_id = cursor.lastrowid

            con2.commit()

            # If user selects "Yes", store data in the 'Ingredients_and_Recipe_Dataset' table
            if publish_value == "Yes":
                cursor.execute("INSERT INTO Ingredients_and_Recipe_Dataset (RecipeName, Ingredients, Instructions) VALUES (?, ?, ?)",
                            ( recipe_name, ingredients, instructions))
                con2.commit()

            con2.close()

            # Print success message for debugging
            print("Recipe added successfully!")
        except Exception as e:
            # Print error message for debugging
            print("Error:", e)
            print(email)
            # Update the error label with the error message
            error_label.config(text=str(e), fg="red")
            error_label.place(x=405, y=370)  # Adjust position as needed
            
        # Retain previously entered details
        recipe_name_text.delete("1.0", END)
        recipe_name_text.insert(END, recipe_name)
        ingredients_text.delete("1.0", END)
        ingredients_text.insert(END, ingredients)
        instructions_text.delete("1.0", END)
        instructions_text.insert(END, instructions)

        # Clear the error message
        error_label.config(text="")

        # Open a new window to prompt user's action
        add_another_window = Toplevel()
        add_another_window.title("Recipe Added")
        add_another_window.geometry(geometry)
        add_another_window.resizable(False, False)

        home_button = Button(new_window, text="Back", command=add_another_window.destroy)
        home_button.place(x=10, y=10)


        # Label to prompt user
        prompt_label = Label(add_another_window, text="Recipe added successfully!\nDo you want to add another recipe or view added recipes?")
        prompt_label.pack()

        # Buttons to add another recipe or view added recipes
        add_another_button = Button(add_another_window, text="Add Another Recipe", command=add_recipe)
        add_another_button.pack()

        view_recipes_button = Button(add_another_window, text="View Added Recipes", command=view_recipes)
        view_recipes_button.pack()

     # Create the 'Recipes' table if it doesn't exist
    con2 = sqlite3.connect("recipe_generator.db")
    cursor = con2.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recipes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            RecipeName TEXT,
            Ingredients TEXT,
            Instructions TEXT
        )''')
    con2.commit()
    con2.close()

    new_window = Toplevel()
    new_window.title("Add Recipe")
    new_window.geometry(geometry)
    new_window.resizable(False, False)
    new_window.iconbitmap(r"logo.png")

    global error_label
    error_label = Label(new_window, text="", fg="red")
    error_label.place(x=100, y=210)

    # Your other GUI elements here
    recipe_name_label = Label(new_window, text="Enter Recipe Name:")
    recipe_name_label.place(x=200, y=80)

    recipe_name_text = Text(new_window, width=25, height=1)
    recipe_name_text.place(x=350, y=80)

    # Your other GUI elements here
    ingredients_label = Label(new_window, text="Enter Ingredients:")
    ingredients_label.place(x=200, y=140)

    ingredients_text = Text(new_window, width=25, height=5)  # Set height to 5 for expanding box
    ingredients_text.place(x=350, y=125)

    # Your other GUI elements here
    instructions_label = Label(new_window, text="Enter Instructions:")
    instructions_label.place(x=200, y=235)

    instructions_text = Text(new_window, width=25, height=5)  # Set height to 5 for expanding box
    instructions_text.place(x=350, y=230)

    # Create a dropdown menu
    publish_label = Label(new_window, text="Do you want to publish recipe?")
    publish_label.place(x=180, y=340)

    publish_options = ["No", "Yes"]
    publish_variable = StringVar(new_window)
    publish_variable.set(publish_options[0])  # Default value

    publish_menu = OptionMenu(new_window, publish_variable, *publish_options)
    publish_menu.place(x=430, y=335)

    home_button = Button(new_window, text="Back", command=new_window.destroy)
    home_button.place(x=10, y=10)

    # Submit Button
    browse_button = Button(new_window, text="Submit", command=add_recipe_to_db)
    browse_button.place(x=430, y=380)

    new_window.mainloop()

def find_recipe():
    def search_recipe():
        query = text_widget.get("1.0", "end-1c").strip().lower()  # Get user input and convert to lowercase
        if not query:
            error_label.config(text="Please enter a recipe name to search.", fg="red")
            error_label.place(x=30, y=35)
            return
        
        # Connect to the database and execute the query
        con = sqlite3.connect("recipe_generator.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Ingredients_and_Recipe_Dataset")
        all_recipes = cursor.fetchall()
        con.close()

        # Process the input query
        query_keywords = query.split(',')

        # Search for matching recipes
        found_recipes = []
        for recipe in all_recipes:
            recipe_name = recipe[1].lower()
            ingredients = recipe[2].lower().split(',')
            instructions = recipe[3].lower()
            # Check if any ingredient or recipe title matches
            if any(keyword.strip() in recipe_name or keyword.strip() in ingredients for keyword in query_keywords):
                found_recipes.append(recipe)

        if not found_recipes:
            messagebox.showinfo("No Results", "No recipes found matching the search criteria.")
        else:
            # Display found recipes in a new window
            result_window = Toplevel()
            result_window.title("Search Results")
            result_window.geometry(geometry)
            result_window.resizable(False, False)

            result_text = Text(result_window, width=100, height=50)
            result_text.pack()

            for recipe in found_recipes:
                result_text.insert(END, f"Recipe Name: {recipe[1]}\nIngredients: {recipe[2]}\nInstructions: {recipe[3]}\n\n")

            home_button = Button(result_window, text="Back", command=result_window.destroy)
            home_button.place(x=400, y=500)

        # Clear the error message
        error_label.config(text="")

    new_window = Toplevel()
    new_window.title("Find Recipe")
    new_window.geometry(geometry)
    new_window.resizable(False, False)

    new_window.iconbitmap(r"logo.png")

    global error_label
    error_label = Label(new_window, text="", fg="red")
    error_label.place(x=100, y=210)
    
    # Create home button
    #create_home_button(new_window, root)  # Pass main window reference

    home_button = Button(new_window, text="Back", command=new_window.destroy)
    home_button.place(x=10, y=10)

    # Your other GUI elements here
    label = Label(new_window, text="Search Here :")
    label.place(x=125, y=60)

    # Ingredient Entry
    ingredient_label = Label(new_window, text="(Enter an Ingredient / Recipe name)")
    ingredient_label.place(x=100, y=100)

    # Create a Text widget to display file contents
    text_widget = Text(new_window, width=15, height=1)
    text_widget.place(x=215, y=60)

    # Buttons
    generate_button = Button(new_window, text="Generate Recipe", command=search_recipe)
    generate_button.place(x=205, y=145)

    new_window.mainloop()

def main():
    root = Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()