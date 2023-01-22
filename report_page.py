from tkinter import *
from tkcalendar import Calendar, DateEntry
import pyreports
import numpy as np
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
from tkinter.filedialog import asksaveasfile
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
import bankstatement_page
import reconcile_page
from fpdf import FPDF

class Report:

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

        label_home = Label(main_frame, text="Report Summary", font=("times new roman",25,"bold"),bg="#e8bcf0").place(x=20, y=5)

        self.home_button = Button(main_frame,text="Home Page",command=self.redirect_home,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=20,y=45)
        self.bank_button = Button(main_frame,text="Bank Statement",command=self.redirect_bank,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=130,y=45)
        self.cash_button = Button(main_frame,text="Cashbook Statement",command=self.redirect_cash,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=270,y=45)
        self.logout_button = Button(main_frame,text="Log Out",command=self.redirect_logout,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=1120,y=45)
        
        display_frame = Frame(self.window, bg="#e8bcf0")
        display_frame.place(x=30,y=120,width=1220,height=540)

        # Select source: this is a DatabaseManager object
        mydb = pyreports.manager('mysql', host='localhost', database='fyp', user='root', password='Ainsafirah97!')

        

        def download():
            # Get data
            mydb.execute('SELECT * FROM bankstatementstorage')
            report = mydb.fetchall()

            # pdf = FPDF()
            # pdf.add_page()
            # page_width = pdf.w - 2 * pdf.l_margin
            # pdf.set_font('Times','B',14.0)
            # pdf.cell(page_width, 0.0, 'Employee Data', align='C')
            # pdf.ln(10)
            
            # pdf.set_font('Courier', '', 12)
            # col_width = page_width/8
            # pdf.ln(1)
            # th = pdf.font_size
            
            # for row in report:
            #     pdf.cell(col_width, row[1], border=1)
            #     pdf.cell(col_width, th, row[2], border=1)
            #     pdf.cell(col_width, th, row[2], border=1)
            #     pdf.cell(col_width, th, row[3], border=1)
            #     pdf.cell(col_width, th, row[4], border=1)
            #     pdf.cell(col_width, th, row[5], border=1)
            #     pdf.cell(col_width, th, row[6], border=1)
            #     pdf.cell(col_width, th, row[7], border=1)
            #     #pdf.ln(th)
                
            # pdf.ln(8)
            # pdf.set_font('Times','',10.0)
            # pdf.cell(page_width, 0.0, '- end of report -', align='C')
            # pdf.output('test.pdf','F')

            y = np.array(report)
            y.shape
            cash_table = np.reshape(y, (-1,8,1))
            #print(bank_table)
            print("Get all transaction in cash statement")
            #print (report)

            ## PyReport as csv
            #csv_report = pyreports.Executor(report)
            ## Save report: this is a FileManager object
            #output = pyreports.manager('csv', 'C:/Users/User/Desktop/cs3.csv')
            #output.write(csv_report.get_data())

            report = asksaveasfile(initialfile = 'Untitled.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt"), ("HTML file","*.html"), ("PDF file","*.pdf")])
            print(report)


        wrapper1 = LabelFrame(display_frame, text="Summary Report", bg="#e8bcf0")
        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

        # for Transaction List Section
        #trv = ttk.Treeview(wrapper1, columns=(6), show="headings", height="20")
        #trv.pack()

        #trv.heading(1, text="Report")
        #trv.bind('<Double 1>', getrow)

        downloadbutton = Button(display_frame, text="Download Report", command=download)
        downloadbutton.pack(side=tk.RIGHT, padx=20, pady=10)



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

    def redirect_bank(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = bankstatement_page.BankStatement(root)
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
    obj = Report(root)
    root.mainloop()