from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
# Create a connection to the SQLite database
conn = sqlite3.connect('recipes.db')  # Change 'your_database.db' to your actual database file

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipe (
        name TEXT NOT NULL PRIMARY KEY,
        ingredients TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Function to insert data into the database
def insert_data():
    # Reconnect to the database
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()


    # retrive data from the 'users' table
    cursor.execute('SELECT * FROM users WHERE name = ? or ingridients = ?', (name,ingredients))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    # Display a success message
    messagebox.showinfo("Success", "Data inserted successfully")












#to insert a image to wizard
class Home():
    def __init__(self,app):
        self.app=app
        self.home_frame = Frame(app)
        self.page_frame1 = Frame(app)
        self.page_frame2 = Frame(app)
        self.current_page = self.home_frame
        self.bg_img=Image.open('back.jpg')
        self.bg_img=self.bg_img.resize((1500,2000))
        self.bg_img=ImageTk.PhotoImage(self.bg_img)
        self.bg_lbl=Label(app,image=self.bg_img)
        self.bg_lbl.place(x=0,y=0)

    def show_home_page(self):
        #Hide the current page's frame
        # (assuming you have a reference to the current page's frame, e.g., self.page_frame)
        self.current_page.pack_forget()
        self.home_frame.pack()
        # Show the home page's frame
        self.current_page = self.home_frame
    def go_back_to_main_page(self):
        # Use this method to go back to the main page from any other page
        self.current_page.pack_forget()  # Hide the current page's frame
        self.home_frame.pack()  # Show the home page's frame
        self.current_page = self.home_frame

app = Tk()
app.geometry('650x350+250+200')
app.title("Recipe Generator")
home = Home(app)

# Function to generate a recipe based on ingredients
def generate_recipe():

    def main_page(self):
        self(main_page).destroy()
        self.Home.destroy()
    
    mainn= Home(app)
    home.show_home_page()
    # After completing the action on the current page, go back to the main page
    home.go_back_to_main_page()
    
# Create the main application window
#title 
title=Label(app , text='RECIPE GENERATOR (TELUGU DISHES)',font=('Times New Roman',15,'bold'))
title.place(x=0,y=0)

# Create and configure GUI elements (labels, entry fields, buttons)
label = Label(app, text="Search Here :")
label.place(x=125 , y=50)

    
# Create a Text widget to display file contents
text_widget = Text(app , width=15, height=1)
text_widget.place(x=205,y=50)


   
# Create a Browse button to select a file
browse_button = Button(app, text="Browse")
browse_button.place(x=340,y=50)


        
# Function to update the ingredient list
def add_ingredient():
    ingredient_listbox.delete(0, END)
    for ingredient in receipes:
        ingredient_listbox.insert(END, ingredient)

# Ingredient Entry
ingredient_label = Label(app, text="Enter an Ingredient:")
ingredient_label.place(x=90,y=100)
ingredient_entry = Entry(app)
ingredient_entry.place(x=205,y=100)

# Buttons
add_button = Button(app, text="show recipes")
generate_button = Button(app, text="Generate Recipe",command=generate_recipe)
add_button.place(x=200,y=125)
generate_button.place(x=200,y=155)

# Ingredient List
ingredient_list_label = Label(app, text="receipes:")
ingredient_list_label.place(x=485,y=5)
ingredient_listbox = Listbox(app)
ingredient_listbox.place(x=450,y=30)


back_to_main_button = Button(app, text="Back to Main Page", command=home.go_back_to_main_page)
back_to_main_button.place(x=200, y=185)
# Create a label to display the result
app.mainloop()
