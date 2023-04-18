from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox
import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')
class BirthDeclaration:
    def __init__(self, root):
        self.root = root
        self.root.title("Birth Declaration Form")
        self.root.geometry("1295x550+230+220")

        #variables
        self.entry_name_var=StringVar()
        self.entry_id_var=StringVar()
        self.entry_father_name_var=StringVar()
        self.entry_mother_name_var=StringVar()
        self.entry_date_var=StringVar()
        self.entry_place_var=StringVar()

        #variable for information table
        self.citizen_ref=str()
        self.citizen_name=str()
        self.citizen_ID=str()
        self.citizen_DOB=str()
        self.address=str()
        self.status=str()
        self.marriage_status=str()



        # Create form labels
        lableframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,font=("times new roman",12,"bold"),padx=2)
        lableframeleft.place(x=10,y=20,width=450,height=490)

        lableframeright=LabelFrame(self.root,bd=2,relief=RIDGE,font=("times new roman",12,"bold"),text="Show",padx=2)
        lableframeright.place(x=470,y=10,width=800,height=500)

        

#==================================================================
        # Create form labels
        
        
        scroll_x=ttk.Scrollbar(lableframeright,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(lableframeright,orient=VERTICAL)
        

        self.birth_table=ttk.Treeview(lableframeright,column=("Name","ID","Father's Name","Mother's Name","Date of Birth","Place of Birth", "Gender"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        
        scroll_x.config(command=self.birth_table.xview)
        scroll_y.config(command=self.birth_table.yview)

        self.birth_table.heading("Name",text="Name")
        self.birth_table.heading("ID",text="ID")
        self.birth_table.heading("Father's Name",text="Father's Name")
        self.birth_table.heading("Mother's Name",text="Mother's Name")
        self.birth_table.heading("Date of Birth",text="Date of Birth")
        self.birth_table.heading("Place of Birth",text="Place of Birth")
        self.birth_table.heading("Gender",text="Gender")
        self.birth_table["show"]="headings"

        self.birth_table.column("Name",width=100)
        self.birth_table.column("ID",width=100)
        self.birth_table.column("Father's Name",width=100)
        self.birth_table.column("Mother's Name",width=100)
        self.birth_table.column("Date of Birth",width=100)
        self.birth_table.column("Place of Birth",width=100)
        self.birth_table.column("Gender",width=100)

        self.birth_table.pack(fill=BOTH,expand=1)
        
        self.birth_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
            
       
#==================================================================

        label_title=Label(lableframeleft,text="Birth Declaration Form",font=("arial",20,"bold"))
        label_title.grid(row=0,columnspan=2,pady=20)

        #create name label and entry
        label_name=Label(lableframeleft,text="Name",font=("arial",12,"bold"))
        label_name.grid(row=1,column=0,padx=10,pady=5,sticky="w")
        entry_name=Entry(lableframeleft,textvariable=self.entry_name_var,font=("arial",12,"bold"),bd=5,relief=GROOVE)
        entry_name.grid(row=1,column=1,padx=10,pady=5)

        #create id label and entry
        label_id=Label(lableframeleft,text="ID",font=("arial",12,"bold"))
        label_id.grid(row=2,column=0,padx=10,pady=5,sticky="w")
        entry_id=Entry(lableframeleft,textvariable=self.entry_id_var,font=("arial",12,"bold"),bd=5,relief=GROOVE)
        entry_id.grid(row=2,column=1,padx=10,pady=5)

        #create father's name label and entry
        label_father_name=Label(lableframeleft,text="Father's Name",font=("arial",12,"bold"))
        label_father_name.grid(row=3,column=0,padx=10,pady=5,sticky="w")
        entry_father_name=Entry(lableframeleft,textvariable=self.entry_father_name_var,font=("arial",12,"bold"),bd=5,relief=GROOVE)
        entry_father_name.grid(row=3,column=1,padx=10,pady=5)
        
        #create mother's name label and entry
        label_mother_name=Label(lableframeleft,text="Mother's Name",font=("arial",12,"bold"))
        label_mother_name.grid(row=4,column=0,padx=10,pady=5,sticky="w")
        entry_mother_name=Entry(lableframeleft,textvariable=self.entry_mother_name_var,font=("arial",12,"bold"),bd=5,relief=GROOVE)
        entry_mother_name.grid(row=4,column=1,padx=10,pady=5)

        #create date of birth label and entry
        label_date=Label(lableframeleft,text="Date of Birth",font=("arial",12,"bold"))
        label_date.grid(row=5,column=0,padx=10,pady=5,sticky="w")
        entry_date=Entry(lableframeleft,textvariable=self.entry_date_var,font=("arial",12,"bold"),bd=5,relief=GROOVE)
        entry_date.grid(row=5,column=1,padx=10,pady=5)


        #create place of birth label and entry
        label_place=Label(lableframeleft,text="Place of Birth",font=("arial",12,"bold"))
        label_place.grid(row=6,column=0,padx=10,pady=5,sticky="w")
        entry_place=Entry(lableframeleft,textvariable=self.entry_place_var,font=("arial",12,"bold"),bd=5,relief=GROOVE)
        entry_place.grid(row=6,column=1,padx=10,pady=5)    

        #create gender label
        label_gender=Label(lableframeleft,text="Gender",font=("arial",12,"bold"))
        label_gender.grid(row=7,column=0,padx=10,pady=5,sticky="w")
        combo_gender=ttk.Combobox(lableframeleft,font=("arial",12,"bold"),state="readonly")
        combo_gender["value"]=("Male","Female") 
        combo_gender.current(0)
        self.gender = combo_gender.get()
        def update_gender(event):
            self.gender=combo_gender.get()
        combo_gender.bind("<<ComboboxSelected>>",update_gender)
        combo_gender.grid(row=7,column=1,padx=10,pady=5)

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
        
       

    def fetch_data(self):
        connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
        my_cursor=connect.cursor()
        my_cursor.execute("SELECT * FROM birth")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.birth_table.delete(*self.birth_table.get_children())
            for row in rows:
                self.birth_table.insert('',END,values=row)
            connect.commit()
        connect.close()
    def get_cursor(self,ev):
        cursor_row=self.birth_table.focus()
        content=self.birth_table.item(cursor_row)
        row=content["values"]
        self.entry_name_var.set(row[0])
        self.entry_id_var.set(row[1])
        self.entry_father_name_var.set(row[2])
        self.entry_mother_name_var.set(row[3])
        self.entry_date_var.set(row[4])
        self.entry_place_var.set(row[5])
        self.gender=row[6]

    def clear(self):
        self.entry_name_var.set("")
        self.entry_id_var.set("")
        self.entry_father_name_var.set("")
        self.entry_mother_name_var.set("")
        self.entry_date_var.set("")
        self.entry_place_var.set("")


    def add_data(self):
        connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
        my_cursor=connect.cursor()
        my_cursor.execute("INSERT INTO birth VALUES(%s,%s,%s,%s,%s,%s,%s)",(
            self.entry_name_var.get(),
            self.entry_id_var.get(),
            self.entry_father_name_var.get(),
            self.entry_mother_name_var.get(),
            self.entry_date_var.get(),
            self.entry_place_var.get(),
            self.gender

        ))
        self.citizen_ref=""
        self.citizen_name=self.entry_name_var.get()
        self.citizen_ID=self.entry_id_var.get()
        self.citizen_DOB=self.entry_date_var.get()
        self.address=self.entry_place_var.get()
        self.marriage_status="Unmarried"
        self.status=""
        my_cursor.execute("insert into information values(%s,%s,%s,%s,%s,%s,%s,%s)",(

            self.citizen_ref,
            self.citizen_name,
            self.citizen_ID,
            self.citizen_DOB,
            self.gender,
            self.address,
            self.marriage_status,
            self.status
            
            ))
        if self.entry_name_var.get()=="" or self.entry_id_var.get()=="" or self.entry_father_name_var.get()=="" or self.entry_mother_name_var.get()=="" or self.entry_date_var.get()=="" or self.entry_place_var.get()=="":
            messagebox.showerror("Error","All fields are required")
        elif not re.match(r'^\d{2}/\d{2}/\d{4}$', self.entry_date_var.get()):
                messagebox.showerror("Error","Enter Valid Date of Birth(DD/MM/YYYY)")
        else:
            connect.commit()
            self.fetch_data()
            connect.close()
            self.clear()
    def update_data(self):
        connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
        my_cursor=connect.cursor()
        my_cursor.execute("update birth set `Name`=%s , `Father Name`=%s, `Mother Name`=%s, `Date of Birth`=%s, `Place of Birth`=%s, Gender=%s where ID=%s",(
            self.entry_name_var.get(),
            self.entry_father_name_var.get(),
            self.entry_mother_name_var.get(),
            self.entry_date_var.get(),
            self.entry_place_var.get(),
            self.gender,
            self.entry_id_var.get()
        ))
        if self.entry_name_var.get()=="" or self.entry_id_var.get()=="" or self.entry_father_name_var.get()=="" or self.entry_mother_name_var.get()=="" or self.entry_date_var.get()=="" or self.entry_place_var.get()=="":
            messagebox.showerror("Error","All fields are required")
        elif not re.match(r'^\d{2}/\d{2}/\d{4}$', self.entry_date_var.get()):
                messagebox.showerror("Error","Enter Valid Date of Birth(DD/MM/YYYY)")
        else:
            connect.commit()
            self.fetch_data()
            connect.close()
            self.clear()
    def delete_data(self):
        connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
        my_cursor=connect.cursor()
        query="delete from birth where ID=%s"
        value=(self.entry_id_var.get(),)
        my_cursor.execute(query,value)
        connect.commit()
        self.fetch_data()
        connect.close()
        self.clear()
