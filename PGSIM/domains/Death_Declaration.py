from tkinter import *
from tkinter import messagebox
import mysql.connector
import re
from tkinter import ttk
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
class DeathDeclaration:
    def __init__(self, root):
        self.root = root
        self.root.title("Death Declaration Form")
        self.root.geometry("1295x550+230+220")
        
        self.entry_place_var=StringVar()
        self.entry_cause_var=StringVar()
        self.entry_citizen_id_var=StringVar()
        self.entry_date_var=StringVar()

        lbl_title=Label(self.root,text="Death Declaration Form",font=("times new roman",18,"bold"),bg="white",fg="green")
        lbl_title.place(x=0,y=0,width=1295,height=50)

        lableframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,font=("times new roman",12,"bold"),padx=2)
        lableframeleft.place(x=10,y=10,width=450,height=500)

        lableframeright=LabelFrame(self.root,bd=2,relief=RIDGE,text="Show",font=("times new roman",12,"bold"),padx=2)
        lableframeright.place(x=470,y=10,width=800,height=500)

#==================================================================
        self.death_table=ttk.Treeview(lableframeright,columns=("citizen_id","date","place","cause"))
        self.death_table.heading("citizen_id",text="Citizen ID")
        self.death_table.heading("date",text="Date of Death")
        self.death_table.heading("place",text="Place of Death")
        self.death_table.heading("cause",text="Cause of Death")
        self.death_table["show"]="headings"
        self.death_table.column("citizen_id",width=100)
        self.death_table.column("date",width=100)
        self.death_table.column("place",width=100)
        self.death_table.column("cause",width=100)
        self.death_table.pack(fill=BOTH,expand=1)
        self.death_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

#==================================================================


        # Create labels
        lbl_title = Label(self.root, text="Death Declaration Form", font=("Arial", 18), padx=10, pady=10)
        lbl_citizen_id = Label(self.root, text="Citizen ID:", font=("Arial", 12), padx=10, pady=10)
        lbl_date = Label(self.root, text="Date of Death:", font=("Arial", 12), padx=10, pady=10)
        lbl_place=Label(self.root,text="Place of Death:",font=("Arial",12),padx=10,pady=10)
        lbl_cause=Label(self.root,text="Cause of Death:",font=("Arial",12),padx=10,pady=10)

        # Create entry fields
        self.entry_citizen_id = Entry(self.root, font=("Arial", 12),textvariable=self.entry_citizen_id_var, width=25)
        self.entry_date = Entry(self.root, font=("Arial", 12),textvariable=self.entry_date_var, width=25)
        self.entry_place=Entry(self.root,font=("Arial",12),textvariable=self.entry_place_var,width=25)
        self.entry_cause=Entry(self.root,font=("Arial",12),textvariable=self.entry_cause_var,width=25)

## button frame
        btn_frame=Frame(lableframeleft,bd=2,relief=RIDGE,)
        btn_frame.place(x=0,y=400,width=412,height=40)
        
        #add button
        btn_add=Button(btn_frame,text="Add",font=("arial",11,"bold"),bg="black",command=self.add_data,fg="yellow",width=10)
        btn_add.grid(row=0,column=0)
        #update button  
        btn_update=Button(btn_frame,text="Update",font=("arial",11,"bold"),bg="black",command=self.update_data,fg="yellow",width=10)
        btn_update.grid(row=0,column=1)
        #delete button
        btn_delete=Button(btn_frame,text="Delete",font=("arial",11,"bold"),bg="black",command=self.delete_data,fg="yellow",width=10)

        btn_delete.grid(row=0,column=2)
        #clear button
        btn_clear=Button(btn_frame,text="Clear",font=("arial",11,"bold"),bg="black",command=self.clear,fg="yellow",width=10)
        btn_clear.grid(row=0,column=3)

        # Add widgets to the grid
        lbl_title.grid(row=0, column=0, columnspan=2)
        lbl_citizen_id.grid(row=1, column=0)
        lbl_date.grid(row=2, column=0)
        lbl_place.grid(row=3,column=0)
        lbl_cause.grid(row=4,column=0)
        self.entry_citizen_id.grid(row=1, column=1)
        self.entry_date.grid(row=2, column=1)
        self.entry_place.grid(row=3,column=1)
        self.entry_cause.grid(row=4,column=1)


    def get_cursor(self,ev):
        cursor_row=self.death_table.focus()
        contents=self.death_table.item(cursor_row)
        row=contents['values']
        self.entry_citizen_id_var.set(row[0])
        self.entry_date_var.set(row[1])
        self.entry_place_var.set(row[2])
        self.entry_cause_var.set(row[3])

        
    def fetch_data(self):
        connect = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        my_cursor=connect.cursor()
        my_cursor.execute("SELECT * FROM death")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.death_table.delete(*self.death_table.get_children())
            for row in rows:
                self.death_table.insert('',END,values=row)
            connect.commit()
        connect.close()
    
    def clear(self):
        self.entry_citizen_id_var.set("")
        self.entry_date_var.set("")
        self.entry_place_var.set("")
        self.entry_cause_var.set("")



    def add_data(self):
        # Connect to database
        connect = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        my_cursor=connect.cursor() 

        # Get citizen information
        citizen_id = self.entry_citizen_id_var.get()
        my_cursor.execute("SELECT * FROM information WHERE `Citizen ID` = %s", (citizen_id,))
        result = my_cursor.fetchone()
        try :
            if result:
                # Insert death declaration
                if not re.match(r'^\d{2}/\d{2}/\d{4}$', self.entry_date_var.get()):
                    messagebox.showerror("Error", "Please enter date in DD/MM/YYYY format.")
                else:
                    my_cursor.execute("INSERT INTO death VALUES (%s, %s, %s, %s)", (citizen_id, self.entry_date_var.get(), self.entry_place_var.get(), self.entry_cause_var.get()))
                    my_cursor.execute("UPDATE information SET `Status` = 'Deceased' WHERE `Citizen ID` = %s", (citizen_id,))
                    connect.commit()
                    self.fetch_data()
                    self.clear()
                    connect.close()
            else:
                messagebox.showerror("Error", "Citizen ID does not exist.")
        except:
            messagebox.showerror("Error", "Citizen ID exists.")

    def update_data(self):
        connect = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )        
        my_cursor=connect.cursor()
        my_cursor.execute("update death set `Date of Death`=%s,`Place of Death`=%s,`Cause of Death`=%s where `Citizen ID`=%s",
                          (self.entry_date_var.get(),
                           self.entry_place_var.get(),
                           self.entry_cause_var.get(),
                           self.entry_citizen_id_var.get()))
        connect.commit()
        self.fetch_data()
        self.clear()
        connect.close()
    def delete_data(self):
        selected_items = self.information_table.selection()
        if not selected_items:
            messagebox.showinfo("Error", "Please select record(s) to delete")
            return
        
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected record(s)?")
        if not confirm:
            return
        
        connect = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        my_cursor = connect.cursor()
        
        for item in selected_items:
            my_cursor.execute("DELETE FROM death WHERE `Citizen ID` = %s", 
                              (self.death_table.item(item)['values'][0],))
        connect.commit()
        connect.close()
        self.fetch_data()
        self.clear()
            
    def search_data(self):
        connect = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        my_cursor = connect.cursor()
        if self.search_by=="Citizen ID":
            my_cursor.execute("select * from death where `Citizen ID` LIKE '%"+str(self.search_txt.get())+"%'")
        elif self.search_by=="Date of Death":
            my_cursor.execute("select * from death where `Date of Death` LIKE '%"+str(self.search_txt.get())+"%'")
        elif self.search_by=="Place of Death":
            my_cursor.execute("select * from death where `Place if Death` LIKE '%"+str(self.search_txt.get())+"%'")
        elif self.search_by=="Cause of Death":
            my_cursor.execute("select * from death where `Cause of Death` LIKE '%"+str(self.search_txt.get())+"%'")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.death_table.delete(*self.death_table.get_children())
            for row in rows:
                self.death_table.insert('',END,values=row)
            connect.commit()
        connect.close()
