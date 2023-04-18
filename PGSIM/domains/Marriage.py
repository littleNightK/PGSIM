import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Marriage:
    def __init__(self, master):
        self.master=master
        self.master.title("Marriage Information")
        self.master.geometry("1295x550+230+220")

        #===========================================

        #===========================================

        # create the marriage information label
        self.marriage_info_label = Label(self.master, text="Marriage Information", font=("times new roman", 20, "bold"), bg="white", fg="green")
        self.marriage_info_label.place(x=0, y=0, width=1295, height=50)

        # create the marriage information frame
        self.marriage_info_frame = Frame(self.master, bd=4, relief=RIDGE)
        self.marriage_info_frame.place(x=0, y=50, width=1295, height=500)

        # create the citizen id label and entry
        self.citizen_id_label = Label(self.marriage_info_frame, text="Citizen ID", font=("times new roman", 15, "bold"), bg="white", fg="green")
        self.citizen_id_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.citizen_id_entry = Entry(self.marriage_info_frame, font=("times new roman", 15, "bold"), bg="lightyellow")
        self.citizen_id_entry.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # create the spouse id label and entry
        self.spouse_id_label = Label(self.marriage_info_frame, text="Spouse ID", font=("times new roman", 15, "bold"), bg="white", fg="green")
        self.spouse_id_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.spouse_id_entry = Entry(self.marriage_info_frame, font=("times new roman", 15, "bold"), bg="lightyellow")
        self.spouse_id_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        # create the marriage date label and entry
        self.marriage_date_label = Label(self.marriage_info_frame, text="Marriage Date", font=("times new roman", 15, "bold"), bg="white", fg="green")
        self.marriage_date_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.marriage_date_entry = Entry(self.marriage_info_frame, font=("times new roman", 15, "bold"), bg="lightyellow")
        self.marriage_date_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")


        # create the save button
        self.save_button = Button(self.marriage_info_frame, text="Save", font=("times new roman", 15, "bold"), bg="green", fg="white", command=self.save_marriage_info)
        self.save_button.grid(row=3, column=0, padx=20, pady=10)

        # create the clear button
        self.clear_button = Button(self.marriage_info_frame, text="Clear", font=("times new roman", 15, "bold"), bg="green", fg="white", command=self.clear_marriage_info)
        self.clear_button.grid(row=3, column=1, padx=20, pady=10)

        #data table
        Table_Frame=Frame(self.marriage_info_frame,bd=4,relief=RIDGE)
        Table_Frame.place(x=400,y=0,width=890,height=500)

        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        self.marriage_info_table=ttk.Treeview(Table_Frame,columns=("citizen_id","spouse_id","date"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.marriage_info_table.xview)
        scroll_y.config(command=self.marriage_info_table.yview)
        self.marriage_info_table.heading("citizen_id",text="Citizen ID")
        self.marriage_info_table.heading("spouse_id",text="Spouse ID")
        self.marriage_info_table.heading("date",text="Date")
        self.marriage_info_table["show"]="headings"
        self.marriage_info_table.column("citizen_id",width=100)
        self.marriage_info_table.column("spouse_id",width=100)
        self.marriage_info_table.column("date",width=100)
        self.marriage_info_table.pack(fill=BOTH,expand=1)
        self.marriage_info_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_marriage_info()


    def get_cursor(self):
        cursor_row=self.marriage_info_table.focus()
        contents=self.marriage_info_table.item(cursor_row)
        row=contents['values']
        self.citizen_id_entry.delete(0,END)
        self.citizen_id_entry.insert(0,row[0])
        self.spouse_id_entry.delete(0,END)
        self.spouse_id_entry.insert(0,row[1])
        self.marriage_date_entry.delete(0,END)
        self.marriage_date_entry.insert(0,row[2])

    def fetch_marriage_info(self):
        connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
         
        my_cursor=connect.cursor()
        my_cursor.execute("select * from marriages")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.marriage_info_table.delete(*self.marriage_info_table.get_children())
            for row in rows:
                self.marriage_info_table.insert('',END,values=row)
            connect.commit()
        connect.close()


    def clear_marriage_info(self):
        # clear the entry widgets
        self.citizen_id_entry.delete(0, END)
        self.spouse_id_entry.delete(0, END)
        self.marriage_date_entry.delete(0, END)

    def save_marriage_info(self):
        # get the marriage information from the entry widgets
        citizen_id = self.citizen_id_entry.get()
        spouse_id = self.spouse_id_entry.get()
        marriage_date = self.marriage_date_entry.get()

        # connect to the SQL database
        try:
            connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
             
            my_cursor=connect.cursor()  
            citizen_id = self.citizen_id_entry.get()
            spouse_id = self.spouse_id_entry.get()
            my_cursor.execute("SELECT * FROM information WHERE `Citizen ID` = %s", (citizen_id,))
            citizen1_id = my_cursor.fetchone()
            my_cursor.execute("SELECT * FROM information WHERE `Citizen ID` = %s", (spouse_id,))
            citizen2_id = my_cursor.fetchone()
            my_cursor.execute("SELECT `Marriage Status` FROM information WHERE `Citizen ID` = %s", (citizen_id,))
            citizen_status = my_cursor.fetchone()
            if citizen_status is not None and citizen_status[0] == "Married":
                messagebox.showerror("Error", "Citizen is already married")
            my_cursor.execute("SELECT `Status` FROM information WHERE `Citizen ID` = %s", (citizen_id,))
            citizen_status = my_cursor.fetchone()
            if citizen_status is not None and citizen_status[0] == "Deceased":
                messagebox.showerror("Error", "Citizen is deceased")
            my_cursor.execute("SELECT `Status` FROM information WHERE `Citizen ID` = %s", (spouse_id,))
            spouse_status = my_cursor.fetchone()
            if spouse_status is not None and spouse_status[0] == "Deceased":
                messagebox.showerror("Error", "Spouse is deceased")

                
            my_cursor.execute("SELECT `Marriage Status` FROM information WHERE `Citizen ID` = %s", (spouse_id,))
            spouse_status = my_cursor.fetchone()
            if spouse_status is not None and spouse_status[0] == "Married":
                messagebox.showerror("Error", "Spouse is already married")
            else:
                spouse_status = None

            if spouse_status is not None and spouse_status[0] == "Married":
                messagebox.showerror("Error", "Spouse is already married")
                
            if citizen1_id == None:
                messagebox.showerror("Error", "Citizen ID does not exist")
            elif citizen2_id == None:
                messagebox.showerror("Error", "Spouse ID does not exist")
            elif citizen_status == "Married":
                messagebox.showerror("Error", "Citizen is already married")
            elif spouse_status == "Married":
                messagebox.showerror("Error", "Spouse is already married")
            elif citizen_id == "":
                messagebox.showerror("Error", "Citizen ID is required")
            elif spouse_id == "":
                messagebox.showerror("Error", "Spouse ID is required")
            elif marriage_date == "":
                messagebox.showerror("Error", "Marriage date is required")
            elif not re.match(r"^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$", marriage_date):
                messagebox.showerror("Error", "Marriage date must be in DD/MM/YYYY format")
            


            else:
                my_cursor.execute("INSERT INTO marriages VALUES (%s, %s, %s)", (citizen_id, spouse_id, marriage_date))
                my_cursor.execute("UPDATE information SET `Marriage Status` = 'Married' WHERE `Citizen ID` = %s", (citizen_id,))
                my_cursor.execute("UPDATE information SET `Marriage Status` = 'Married' WHERE `Citizen ID` = %s", (spouse_id,))
                connect.commit()
                messagebox.showinfo("Success", "Marriage certification saved successfully")
                self.fetch_marriage_info()
                self.clear_marriage_info()

        except mysql.connector.errors.IntegrityError as e:
            # catch the IntegrityError exception and replace its message
            error_message = "Marriage certification existed"
            e.args = (error_message,)
            messagebox.showerror("Error", error_message)
                

        # close the database connection
        connect.close()

