from tkinter import *
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
import csv
import pymysql
import mysql.connector
import os
import credentials as cr
#import dash_bootstrap_components as dbc
import tkinter as tk
from tkinter import font as tkfont
import home_page
import bankstatement_page
import login_page
import reconcile_page
import report_page

class CashBook:

    def __init__(self, root):
        self.window = root
        self.window.title("Bank Reconciliation")
        self.window.geometry("1080x650+115+70")
        self.window.config(bg = "black")

        self.bg_img = ImageTk.PhotoImage(file="Images/3.jpg")
        background = Label(self.window,image=self.bg_img).place(x=0,y=3)

        main_frame = Frame(self.window, bg="#e8bcf0")
        main_frame.place(x=30,y=30,width=1220,height=75)

        self.window.state('zoomed')

        label_home = Label(main_frame, text="Cashbook Statement", font=("times new roman",25,"bold"),bg="#e8bcf0").place(x=20, y=5)

        self.bank_button = Button(main_frame,text="Home Page",command=self.redirect_home,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=20,y=45)
        self.cash_button = Button(main_frame,text="Bank Statement",command=self.redirect_bank,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=130,y=45)
        self.report_button = Button(main_frame,text="Report Summary",command=self.redirect_report,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=280,y=45)
        self.logout_button = Button(main_frame,text="Log Out",command=self.redirect_logout,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=1120,y=45)
        

        display_frame = Frame(self.window, bg="#e8bcf0")
        display_frame.place(x=30,y=120,width=1220,height=540)

        #to make sure data in table clear
        self.connection = mysql.connector.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
        self.cursor = self.connection.cursor()

        truncate = "truncate cashbookstorage"
        self.cursor.execute(truncate)

        #reset_increment = "alter table bankstatementstorage auto_increment=1"
        #self.cursor.execute(reset_increment)

         # to read all rows availble in the table
        

        def update(rows):
            # clearing table before showing matching search
            trv.delete(*trv.get_children())
            for i in rows:
                trv.insert('', 'end', values=i)

        #def search():
            #q2 = q
            #query_search = "SELECT * FROM cashbook WHERE description LIKE '%"+str(q2)+"' OR reference LIKE '%"+str(q2)+"%'"
            #self.cursor.execute(query_search)
            #rows = self.cursor.fetchall()
            #update(rows)

        def clear():
            query_clear = "SELECT * FROM cashbookstorage"
            self.cursor.execute(query_clear)
            rows = self.cursor.fetchall()
            update(rows)

        def getrow(event):
            rowid = trv.identify_row(event.y)
            item = trv.item(trv.focus())
            t1.set(item['values'][0])
            t2.set(item['values'][1])
            t3.set(item['values'][2])
            t4.set(item['values'][3])
            t5.set(item['values'][4])
            t6.set(item['values'][5])
            t7.set(item['values'][6])
            t8.set(item['values'][7])

        
        def update_id():
            c_id = t1.get()
            c_reference = t2.get()
            c_description = t3.get()
            c_amount = t4.get()
            c_date = t5.get()
            c_time = t6.get()
            c_approvalcode = t7.get()
            c_transfertype = t8.get()
            if messagebox.askyesno("Confirm Please", "Are you sure you want to update this data?"):
                query_update_id = "UPDATE cashbookstorage SET cbs_reference = %s, cbs_description = %s, cbs_amount = %s, cbs_date = %s, cbs_time = %s, cbs_approvalcode = %s, cbs_transfertype = %s WHERE cbs_id = %s"
                self.cursor.execute(query_update_id, (c_reference, c_description, c_amount, c_date, c_time, c_approvalcode, c_transfertype, c_id))
                self.connection.commit()
                clear()
            else:
                return True

        def add_new():
            c_id = t1.get()
            c_reference = t2.get()
            c_description = t3.get()
            c_amount = t4.get()
            c_date = t5.get()
            c_time = t6.get()
            c_approvalcode = t7.get()
            c_transfertype = t8.get()
            # can't make id auto increment maybe bcs when create table, set id as not null so it can't accept null statement to make it auto increment
            query_add_new = "INSERT INTO cashbookstorage(cbs_id, cbs_reference, cbs_description, cbs_amount, cbs_date, cbs_time, cbs_approvalcode, cbs_transfertype) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query_add_new, (c_id, c_reference, c_description, c_amount, c_date, c_time, c_approvalcode, c_transfertype))
            clear()
        
        def delete_id():
            c_id = t1.get()
            # create message box if user confirm to delete the id data
            if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this customer?"):
                query_delete_id = "DELETE FROM cashbookstorage WHERE cbs_id = " + c_id
                self.cursor.execute(query_delete_id)
                self.connection.commit()
                clear()
            else:
                return True

        def uploadcash():
            cashbookdata = q
            #bankstatementdata.clear()
            fln1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open Cashbook Statement", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
            with open(fln1) as myfile:
                csvread = csv.reader(myfile, delimiter=",")
                next(csvread)
                for i in csvread:
                    cashbookdata.append(i)
                    uid = i[0]
                    ref = i[1]
                    des = i[2]
                    amt = i[3]
                    date = i [4]
                    time = i [5]
                    appcode = i[6]
                    transfertype = i[7]

                    query = "insert into cashbookstorage (cbs_id, cbs_reference, cbs_description, cbs_amount, cbs_date, cbs_time, cbs_approvalcode, cbs_transfertype) values(%s,%s,%s,%s,%s,%s,%s,%s)"

                    self.cursor.execute(query, (uid, ref, des, amt, date, time, appcode, transfertype))

                #clear function
                query = "select * from cashbookstorage"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                update(rows)
            
            #rows = self.cursor.fetchall()
            #update(rows)

        def savecash():
            cashbookdata = q
            if messagebox.askyesno("Confirmation", "Correct Data?"):
                #for i in cashbookdata:
                    #uid = i[0]
                    #ref = i[1]
                    #des = i[2]
                    #amt = i[3]
                    #date = i [4]
                    #appcode = i[5]

                    #query = "insert into cashbook (c_id, c_reference, c_description, c_amount, c_date, c_approvalCode) values(NULL,%s,%s,%s,%s,%s)"

                    #self.cursor.execute(query, (ref, des, amt, date, appcode))

                self.connection.commit()
                #clear funtion
                #query = "select c_id, c_reference, c_description, c_amount, c_date, c_approvalCode from cashbook"
                #self.cursor.execute(query)
                #rows = self.cursor.fetchall()
                #update(rows)
                messagebox.showinfo("Data saved", "Data Has Been Saved to the Database")
            else:
                messagebox.showinfo("Data cannot be saved")

        def reconcile():
            obj = reconcile_page.Reconcile(root)
            root.mainloop()
            


        self.connection = mysql.connector.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
        self.cursor = self.connection.cursor()

        q = []
        t1 = StringVar()
        t2 = StringVar()
        t3 = StringVar()
        t4 = StringVar()
        t5 = StringVar()
        t6 = StringVar()
        t7 = StringVar()
        t8 = StringVar()

        # divide the frame into multiples section with seperation and title
        wrapper1 = LabelFrame(display_frame, text="Transaction List", bg="#e8bcf0")
        #wrapper2 = LabelFrame(display_frame, text="Search", bg="white")
        wrapper3 = LabelFrame(display_frame, text="Customer Data", bg="#e8bcf0")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        #wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # for Transaction List Section
        trv = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6,7,8), show="headings", height="5")
        trv.pack()

        trv.heading(1, text="ID")
        trv.heading(2, text="Reference")
        trv.heading(3, text="Description")
        trv.heading(4, text="Amount")
        trv.heading(5, text="Date")
        trv.heading(6, text="Time")
        trv.heading(7, text="Approval Code")
        trv.heading(8, text="Transfer Type")

        trv.bind('<Double 1>', getrow)

        query = "select cbs_id, cbs_reference, cbs_description, cbs_amount, cbs_date, cbs_time, cbs_approvalcode, cbs_transfertype from cashbookstorage"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # for Search Section
        #lbl_search = Label(wrapper2, text="Search :", bg="white")
        #lbl_search.pack(side=tk.LEFT, padx=10)
        #ent_search = Entry(wrapper2, textvariable=q)
        #ent_search.pack(side=tk.LEFT, padx=6)
        #btn_search = Button(wrapper2, text="Search", command=search)
        #btn_search.pack(side=tk.LEFT, padx=6)
        #cbtn_search = Button(wrapper2, text="Clear", command=clear)
        #cbtn_search.pack(side=tk.LEFT, padx=6)

        # for User Data Section
        lbl_user1 = Label(wrapper3, text="ID :", bg="#e8bcf0")
        lbl_user1.grid(row=0, column=0, padx=5, pady=3)
        ent_user1 = Entry(wrapper3, textvariable=t1)
        ent_user1.grid(row=0, column=1, padx=5, pady=3)
        
        lbl_user2 = Label(wrapper3, text="Reference :", bg="#e8bcf0")
        lbl_user2.grid(row=1, column=0, padx=5, pady=3)
        #ent_user2 = Entry(wrapper3, textvariable=t2)
        #ent_user2.grid(row=1, column=1, padx=5, pady=3)
        #to create dropbox
        ent_user2 = ttk.Combobox(wrapper3, textvariable=t2, state='readonly')
        ent_user2['values'] = ("Select","debit dard","online transfer","cheque")
        ent_user2.grid(row=1, column=1, padx=5, pady=3)
        ent_user2.current(0)
        
        lbl_user3 = Label(wrapper3, text="Description :", bg="#e8bcf0")
        lbl_user3.grid(row=2, column=0, padx=5, pady=3)
        ent_user3 = Entry(wrapper3, textvariable=t3)
        ent_user3.grid(row=2, column=1, padx=5, pady=3)


        lbl_user4 = Label(wrapper3, text="Amount :", bg="#e8bcf0")
        lbl_user4.grid(row=3, column=0, padx=5, pady=3)
        ent_user4 = Entry(wrapper3, textvariable=t4)
        ent_user4.grid(row=3, column=1, padx=5, pady=3)
        
        lbl_user5 = Label(wrapper3, text="Date :", bg="#e8bcf0")
        lbl_user5.grid(row=4, column=0, padx=5, pady=3)
        ent_user5 = DateEntry(wrapper3, width=17, textvariable=t5, year=2022, date_pattern='yyyy-mm-dd')
        ent_user5.grid(row=4, column=1, padx=5, pady=3)
        
        lbl_user6 = Label(wrapper3, text="Time :", bg="#e8bcf0")
        lbl_user6.grid(row=5, column=0, padx=5, pady=3)
        ent_user6 = Entry(wrapper3, textvariable=t6)
        ent_user6.grid(row=5, column=1, padx=5, pady=3)

        lbl_user7 = Label(wrapper3, text="Approval Code :", bg="#e8bcf0")
        lbl_user7.grid(row=6, column=0, padx=5, pady=3)
        ent_user7 = Entry(wrapper3, textvariable=t7)
        ent_user7.grid(row=6, column=1, padx=5, pady=3)
        
        lbl_user8 = Label(wrapper3, text="Transfer Type :", bg="#e8bcf0")
        lbl_user8.grid(row=7, column=0, padx=5, pady=3)
        #ent_user8 = Entry(wrapper3, textvariable=t8)
        #ent_user8.grid(row=7, column=1, padx=5, pady=3)
        ent_user8 = ttk.Combobox(wrapper3, textvariable=t8, state='readonly')
        ent_user8['values'] = ("Select","credit","debit")
        ent_user8.grid(row=7, column=1, padx=5, pady=3)
        ent_user8.current(0)

        btn_add = Button(wrapper3, text="Add New", command=add_new)
        btn_add.grid(row=8, column=0, padx=5, pady=3)
        btn_update = Button(wrapper3, text="Update", command=update_id)
        btn_update.grid(row=8, column=1, padx=5, pady=3)
        btn_delete = Button(wrapper3, text="Delete", command=delete_id)
        btn_delete.grid(row=8, column=2, padx=5, pady=3)

        uploadbutton = Button(wrapper1, text="Upload File", command=uploadcash)
        uploadbutton.pack(side=tk.LEFT, padx=10, pady=10)

        savebutton = Button(wrapper1, text="Save File", command=savecash)
        savebutton.pack(side=tk.LEFT, padx=10, pady=10)

    #command reconcile
        reconcilebutton = Button(wrapper1, text="Reconcile", command=reconcile)
        reconcilebutton.pack(side=tk.LEFT, padx=10, pady=10)

    def redirect_home(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = home_page.Home(root)
        root.mainloop()

    def redirect_bank(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = bankstatement_page.BankStatement(root)
        root.mainloop()

    def redirect_report(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = report_page.Report(root)
        root.mainloop()

    def redirect_logout(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = login_page.Login(root)
        root.mainloop()
    
if __name__ == "__main__":
    root = Tk()
    obj = CashBook(root)
    root.mainloop()