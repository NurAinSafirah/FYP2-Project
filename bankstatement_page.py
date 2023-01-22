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
import cashbook_page
import home_page
import login_page
import reconcile_page

class BankStatement:

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

        label_home = Label(main_frame, text="Bank Statement", font=("times new roman",25,"bold"),bg="#e8bcf0").place(x=20, y=5)

        self.bank_button = Button(main_frame,text="Home Page",command=self.redirect_home,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=20,y=45)
        self.cash_button = Button(main_frame,text="Cashbook Statement",command=self.redirect_cash,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=130,y=45)
        self.report_button = Button(main_frame,text="Report Summary",command=self.redirect_report,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=310,y=45)
        self.logout_button = Button(main_frame,text="Log Out",command=self.redirect_logout,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=1120,y=45)
        
        display_frame = Frame(self.window, bg="#e8bcf0")
        display_frame.place(x=30,y=120,width=1220,height=540)

        #to make sure data in table clear
        self.connection = mysql.connector.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
        self.cursor = self.connection.cursor()

        truncate = "truncate bankstatementstorage"
        self.cursor.execute(truncate)

        #reset_increment = "alter table bankstatementstorage auto_increment=1"
        #self.cursor.execute(reset_increment)

         # to read all rows availble in the table
    
        def update(rows):
            # clearing table before showing matching search
            trv.delete(*trv.get_children())
            for i in rows:
                trv.insert('', 'end', values=i)

        # def search():
        #     q3 = q2.get
        #     query_search = "SELECT * FROM bankstatementstorage WHERE bss_id LIKE '%"+q3+"%' OR bss_amount LIKE '%"+q3+"' OR bss_date LIKE '%"+q3+"%' OR bss_transfertype LIKE '%"+q3+"%' OR bss_approvalcode LIKE '%"+q3+"%' OR bss_description LIKE '%"+q3+"%' OR bss_reference LIKE '%"+q3+"%'"
        #     self.cursor.execute(query_search)
        #     rows = self.cursor.fetchall()
        #     update(rows)

        def clear():
            query_clear = "SELECT * FROM bankstatementstorage"
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


        # not functioning
        def update_id():
            id = t1.get()
            reference = t2.get()
            description = t3.get()
            amount = t4.get()
            date = t5.get()
            time = t6.get()
            approvalcode = t7.get()
            transfertype = t8.get()
            if messagebox.askyesno("Confirm Please", "Are you sure you want to update this id?"):
                query_update_id = "UPDATE bankstatementstorage SET bss_reference = %s, bss_description = %s, bss_amount = %s, bss_date = %s, bss_time = %s, bss_approvalcode = %s, bss_transfertype = %s WHERE bss_id = %s"
                self.cursor.execute(query_update_id, (reference, description, amount, date, time, approvalcode, transfertype, id))
                self.connection.commit()
                clear()
            else:
                return True

        def add_new():
            id = t1.get()
            reference = t2.get()
            description = t3.get()
            amount = t4.get()
            date = t5.get()
            time = t6.get()
            approvalcode = t7.get()
            transfertype = t8.get()
            # can't make id auto increment maybe bcs when create table, set id as not null so it can't accept null statement to make it auto increment
            query_add_new = "INSERT INTO bankstatementstorage(bss_id, bss_reference, bss_description, bss_amount, bss_date, bss_time, bss_approvalcode, bss_transfertype) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query_add_new, (id, reference, description, amount, date, time, approvalcode, transfertype))
            clear()
        
        def delete_id():
            id = t1.get()
            # create message box if user confirm to delete the id data
            if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this customer?"):
                query_delete_id = "DELETE FROM bankstatementstorage WHERE bss_id = " + id
                self.cursor.execute(query_delete_id)
                self.connection.commit()
                clear()
            else:
                return True

        def uploadbank():
            bankstatementdata = q
            bankstatementdata.clear()
            fln1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open Bank Statement", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
            with open(fln1) as myfile:
                csvread = csv.reader(myfile, delimiter=",")
                next(csvread)
                for i in csvread:
                    bankstatementdata.append(i)
                    uid = i[0]
                    ref = i[1]
                    des = i[2]
                    amt = i[3]
                    date = i [4]
                    time = i [5]
                    appcode = i[6]
                    transfertype = i[7]

                    query = "insert into bankstatementstorage (bss_id, bss_reference, bss_description, bss_amount, bss_date, bss_time, bss_approvalcode, bss_transfertype) values(%s,%s,%s,%s,%s,%s,%s,%s)"

                    self.cursor.execute(query, (uid, ref, des, amt, date, time, appcode, transfertype))

                #clear function
                query = "select * from bankstatementstorage"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                update(rows)
            
            #rows = self.cursor.fetchall()
            #update(rows)

        #testing different upload format
        # def uploadbank():
        #     frame = Frame(self.window, bg="#e8bcf0", highlightbackground="#710193", highlightthickness=1)
        #     frame.place(x=420,y=90,width=460,height=550)
            
            # z1 = []
            # z2 = []
            # z3 = []
            # z4 = []
            # z5 = []
            # z6 = []
            # z7 = []
            # z8 = []

        #     bankstatementdata = q
        #     #bankstatementdata.clear()
        #     fln1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open Bank Statement", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        #     with open(fln1) as myfile:
        #         csvread = csv.reader(myfile, delimiter=",")
        #         for i in csvread:
        #             bankstatementdata.append(i)
        #             uid = i[0]
        #             ref = i[1]
        #             des = i[2]
        #             amt = i[3]
        #             date = i [4]
        #             time = i [5]
        #             appcode = i[6]
        #             transfertype = i[7]
                    

        #         uid1 = Label(frame, text="UID :", bg="#e8bcf0")
        #         uid1.grid(row=1, column=0, padx=5, pady=3)
        #         c1 = ttk.Combobox(frame, textvariable=uid, state='readonly')
        #         c1['values'] = ("Select",uid,ref,des, amt, date, time, appcode, transfertype)
        #         c1.grid(row=1, column=1, padx=5, pady=3)
        #         c1.current(0)

        #         ref1 = Label(frame, text="REF :", bg="#e8bcf0")
        #         ref1.grid(row=2, column=0, padx=5, pady=3)
        #         c2 = ttk.Combobox(frame, textvariable=ref, state='readonly')
        #         c2['values'] = ("Select",uid,ref,des, amt, date, time, appcode, transfertype)
        #         c2.grid(row=2, column=1, padx=5, pady=3)
        #         c2.current(0)

        #         dec1 = Label(frame, text="DEC :", bg="#e8bcf0")
        #         dec1.grid(row=3, column=0, padx=5, pady=3)
        #         c3 = ttk.Combobox(frame, textvariable=des, state='readonly')
        #         c3['values'] = ("Select",uid,ref,des, amt, date, time, appcode, transfertype)
        #         c3.grid(row=3, column=1, padx=5, pady=3)
        #         c3.current(0)

        #         amt1 = Label(frame, text="AMT :", bg="#e8bcf0")
        #         amt1.grid(row=4, column=0, padx=5, pady=3)
        #         c4 = ttk.Combobox(frame, textvariable=amt, state='readonly')
        #         c4['values'] = ("Select",uid,ref,des, amt, date, time, appcode, transfertype)
        #         c4.grid(row=4, column=1, padx=5, pady=3)
        #         c4.current(0)

        #         date1 = Label(frame, text="DATE :", bg="#e8bcf0")
        #         date1.grid(row=5, column=0, padx=5, pady=3)
        #         c5 = ttk.Combobox(frame, textvariable=date, state='readonly')
        #         c5['values'] = ("Select",uid,ref,des, amt, date, time, appcode, transfertype)
        #         c5.grid(row=5, column=1, padx=5, pady=3)
        #         c5.current(0)

        #         time1 = Label(frame, text="TIME :", bg="#e8bcf0")
        #         time1.grid(row=6, column=0, padx=5, pady=3)
        #         c6 = ttk.Combobox(frame, textvariable=time, state='readonly')
        #         c6['values'] = ("Select", uid, ref, des, amt, date, time, appcode, transfertype)
        #         c6.grid(row=6, column=1, padx=5, pady=3)
        #         c6.current(0)

        #         appcode1 = Label(frame, text="APPCODE :", bg="#e8bcf0")
        #         appcode1.grid(row=7, column=0, padx=5, pady=3)
        #         c7 = ttk.Combobox(frame, textvariable=appcode, state='readonly')
        #         c7['values'] = ("Select", uid, ref, des, amt, date, time, appcode, transfertype)
        #         c7.grid(row=7, column=1, padx=5, pady=3)
        #         c7.current(0)

        #         transfertype1 = Label(frame, text="TRANSFERTYPE :", bg="#e8bcf0")
        #         transfertype1.grid(row=8, column=0, padx=5, pady=3)
        #         c8 = ttk.Combobox(frame, textvariable=transfertype, state='readonly')
        #         c8['values'] = ("Select",uid, ref, des, amt, date, time, appcode, transfertype)
        #         c8.grid(row=8, column=1, padx=5, pady=3)
        #         c8.current(0)

                

        #         query = "insert into bankstatementstorage (bss_id, bss_reference, bss_description, bss_amount, bss_date, bss_time, bss_approvalcode, bss_transfertype) values(%s,%s,%s,%s,%s,%s,%s,%s)"

        #         self.cursor.execute(query, (uid, ref, des, amt, date, appcode, time, transfertype))
        #         #self.cursor.execute(query, (uid1, ref1, dec1, amt1, date1, time1, appcode1, transfertype1))
        #         #self.cursor.execute(query, (z1, z2, z3, z4, z5, z6, z7, z8))
        #         #self.cursor.execute(query, (str(c1[0]), str(c2[1]), str(c3[2]), str(c4[3]), str(c5[4]), str(c6[5]), str(c7[6]), str(c8[7])))

        #         #clear function
        #         query = "select * from bankstatementstorage"
        #         self.cursor.execute(query)
        #         rows = self.cursor.fetchall()
        #         update(rows)

                
            
        #     #rows = self.cursor.fetchall()
        #     #update(rows)

        def savebank():
            bankstatementdata = q
            if messagebox.askyesno("Confirmation", "Correct Data?"):
                #for i in bankstatementdata:
                    #uid = i[0]
                    #ref = i[1]
                    #des = i[2]
                    #amt = i[3]
                    #date = i [4]
                    #time = i[5]
                    #appcode = i[6]
                    #transfertype = i[7]

                    #query = "insert into bankstatementstorage (bss_id, bss_reference, bss_description, bss_amount, bss_date, bss_time, bss_approvalcode, bss_transfertype) values(%s,%s,%s,%s,%s,%s,%s,%s)"

                    #self.cursor.execute(query, (uid, ref, des, amt, date, time, appcode, transfertype))

                self.connection.commit()
                #clear (function)
                #query = "select id, reference, description, amount, date, approvalCode from bankstatement"
                #self.cursor.execute(query)
                #rows = self.cursor.fetchall()
                #update(rows)
                messagebox.showinfo("Data saved", "Data Has Been Saved to the Database")
            else:
                messagebox.showinfo("Data cannot be saved")

        def redirect_reconcile():
            #manually concate first
            # id = t1.get()
            # reference = t2.get()
            # description = t3.get()
            # amount = t4.get()
            # date = t5.get()
            # time = t6.get()
            # approvalcode = t7.get()
            # transfertype = t8.get()

            # concate = amount + date + transfertype
            # print ("Concated" + str(concate))

            #self.window.destroy()
            #root = Tk()
            # Importing the home window
            obj = reconcile_page.Reconcile(root)
            root.mainloop()
            

        self.connection = mysql.connector.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
        self.cursor = self.connection.cursor()

        q = []
        q2 = StringVar()
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
        #wrapper2 = LabelFrame(display_frame, text="Search", bg="#e8bcf0")
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

        query = "select bss_id, bss_reference, bss_description, bss_amount, bss_date, bss_time, bss_approvalcode, bss_transfertype from bankstatementstorage"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        #for Search Section
        # lbl_search = Label(wrapper2, text="Search :", bg="#e8bcf0")
        # lbl_search.pack(side=tk.LEFT, padx=10)
        # ent_search = Entry(wrapper2, textvariable=q2)
        # ent_search.pack(side=tk.LEFT, padx=6)
        # btn_search = Button(wrapper2, text="Search", command=search)
        # btn_search.pack(side=tk.LEFT, padx=6)
        # cbtn_search = Button(wrapper2, text="Clear", command=clear)
        # cbtn_search.pack(side=tk.LEFT, padx=6)

        # for User Data Section
        lbl_user1 = Label(wrapper3, text="ID :", bg="#e8bcf0")
        lbl_user1.grid(row=0, column=0, padx=5, pady=3)
        ent_user1 = Entry(wrapper3, textvariable=t1)
        ent_user1.grid(row=0, column=1, padx=5, pady=3)
        
        lbl_user2 = Label(wrapper3, text="Reference :", bg="#e8bcf0")
        lbl_user2.grid(row=1, column=0, padx=5, pady=3)
        #ent_user2 = Entry(wrapper3, textvariable=t2)
        #ent_user2.grid(row=1, column=1, padx=5, pady=3)
        ent_user2 = ttk.Combobox(wrapper3, textvariable=t2, state='readonly')
        ent_user2['values'] = ("Select","debit dard","online transfer", "cheque")
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
        btn_delete.grid(row=8, column=2, padx=3, pady=3)

        uploadbutton = Button(wrapper1, text="Upload File", command=uploadbank)
        uploadbutton.pack(side=tk.LEFT, padx=10, pady=10)

        savebutton = Button(wrapper1, text="Save File", command=savebank)
        savebutton.pack(side=tk.LEFT, padx=10, pady=10)

        #command reconcile
        reconcilebutton = Button(wrapper1, text="Reconcile", command=redirect_reconcile)
        reconcilebutton.pack(side=tk.LEFT, padx=10, pady=10)

        


    def redirect_home(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = home_page.Home(root)
        root.mainloop()

    def redirect_cash(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = cashbook_page.CashBook(root)
        root.mainloop()

    def redirect_report(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = cashbook_page.CashBook(root)
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
    obj = BankStatement(root)
    root.mainloop()