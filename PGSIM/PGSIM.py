import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from ttkthemes import ThemedStyle
from tkinter import ttk
from domains.information import Information
from domains.Death_Declaration import DeathDeclaration
from domains.Marriage import Marriage
from domains.Birth_declaration import BirthDeclaration
import configparser
import Database.Create_table as create_table
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')
# Connect to MySQL server
connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],

)

# Create a new database
database_name = "mydata"
cursor = connect.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
connect.database = database_name

# Create the tables
create_table.create_information_table()
create_table.create_marriage_table()
create_table.create_birth_table()
create_table.create_death_table()

# Create a new Tkinter window
root = tk.Tk()

# Set the window size and title
root.geometry("430x490+500+130")
root.title("PGSIM")


# Create a themed style object
style = ThemedStyle(root)
style.set_theme("equilux")

# Create a PhotoImage object--
image = PhotoImage(file="Interface\logo.png")
# Create a Label widget with the image
label = Label(root, image=image)

# Plack the Label widget
label.place(x=-103, y=90)

canvas3 = tk.Canvas(root, width=500, height=50, bg="#6495ED", highlightthickness=0)
canvas3.place(x = 0, y = 70)
canvas4 = tk.Canvas(root, width=500, height=50, bg="#6495ED", highlightthickness=0)
canvas4.place(x = 0, y = 450)

# Set the window background color
root.configure(bg='#6495ED')

canvas = tk.Canvas(root, width=30, height=500, bg="#003366", highlightthickness=0)
canvas.place(x = 0, y = 0)

canvas2 = tk.Canvas(root, width=30, height=500, bg="#003366", highlightthickness=0)
canvas2.place(x = 400, y = 0)


def information():
    infor_window = tk.Toplevel(root)
    app = Information(infor_window)

def marriage():
    marriage_window = tk.Toplevel(root)
    app = Marriage(marriage_window)

def birth():
    birth_window = tk.Toplevel(root)
    app = BirthDeclaration(birth_window)

def death():
    death_window = tk.Toplevel(root)
    app = DeathDeclaration(death_window)

style = ttk.Style()

# define a custom color for the button
style.map("TButton", background=[("active", "#00008B"), ("!disabled", "#8D918D")])
style.configure("TButton",relief='groove', bordercolor="#8D918D", borderwidth=2)

# Create the buttons with a fixed size
button_width = 40
button_height = 4
add_button = ttk.Button(root, text="Citizens information", command=information, width=button_width, padding=button_height)
update_button = ttk.Button(root, text="Marriage declaration", command=marriage, width=button_width, padding=button_height)
delete_button = ttk.Button(root, text="Birth certificate", command=birth, width=button_width, padding=button_height)
search_button = ttk.Button(root, text="Death declaratiom", command=death, width=button_width, padding=button_height)

# Add the buttons to the window
add_button.place(x=215, y=150+64, anchor = "center")
update_button.place(x=215, y=200+64, anchor = "center")
delete_button.place(x=215, y=250+64, anchor = "center")
search_button.place(x=215, y=300+64, anchor = "center")


frame = tk.Frame(root, width=328, height=72, bg="black", relief="solid", highlightbackground="#003366", highlightthickness=5)
frame.place(x=49, y=30)

text_label = tk.Label(root, text="GOVERNMENTAL INFORMATION MANAGEMENT SYSTEM", fg="#00008B", bg="#8D918D",font=("Segoe UI",15,"bold"),wraplength=400, anchor="center")
text_label.place(x=54, y=35)

root.mainloop()



'''
# Create a frame with a gray background and blue border
board_frame = tk.Frame(root, width=10, height=500, bg="gray", relief="solid", highlightbackground="#003366", highlightthickness=5)
board_frame.place(x=345, y=73)

# Add a label to display stored information 
info_label = tk.Label(board_frame, text="Display", font=("Calibri", 16))
info_label.place(x=10, y=10)
'''
