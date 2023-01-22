from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import tkinter as tk
import pymysql
import os
import csv
import credentials as cr
import mysql.connector
import bankstatement_page
import cashbook_page
import login_page


class Home:
    def __init__(self, root):
        self.window = root
        self.window.title("Home Page with Tab")
        self.window.geometry("1080x600+115+70")
        self.window.config(bg = "black")
        self.bg_img = ImageTk.PhotoImage(file="Images/3.jpg")
        background = Label(self.window,image=self.bg_img).place(x=0,y=3)
        
        main_frame = Frame(self.window, bg="#e8bcf0")
        main_frame.place(x=30,y=30,width=1220,height=75)

        self.window.state('zoomed')

        label_home = Label(main_frame, text="Home Page", font=("times new roman",25,"bold"),bg="#e8bcf0").place(x=20, y=5)

        self.bank_button = Button(main_frame,text="Bank Statement",command=self.redirect_bank,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=20,y=45)
        self.cash_button = Button(main_frame,text="Cashbook Statement",command=self.redirect_cash,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=160,y=45)
        self.report_button = Button(main_frame,text="Report Summary",command=self.redirect_report,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=330,y=45)
        self.logout_button = Button(main_frame,text="Log Out",command=self.redirect_logout,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=1120,y=45)

        display_frame = Frame(self.window, bg="#e8bcf0")
        display_frame.place(x=30,y=120,width=1220,height=540)

        self.txt = "USER PROFILE"
        self.heading = Label(display_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#e8bcf0", fg='black', bd=5, relief=FLAT)
        self.heading.place(x=80, y=20, width=300, height=30)

        # ============ Left Side Image ================================================
        self.side_image = Image.open('Images\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(display_frame, image=photo, bg='#e8bcf0')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=50)

        # ============ Sign In Image =============================================
        #self.sign_in_image = Image.open('Images\\hyy.png')
        #photo = ImageTk.PhotoImage(self.sign_in_image)
        #self.sign_in_image_label = Label(display_frame, image=photo, bg='#e8bcf0')
        #self.sign_in_image_label.image = photo
        #self.sign_in_image_label.place(x=620, y=50)

        #update profile pic
        self.image = PhotoImage(file='Images\\hyy.png')
        self.label = Label(display_frame, image=self.image, bg='#e8bcf0')
        self.label.place(x=660, y=50)
        self.file = Button(display_frame, text='Browse', command=self.choose)
        self.file.place(x=785, y=130)

        # ============ Sign In label =============================================
        #self.sign_in_label = Label(display_frame, text="Welcome", bg="#e8bcf0", fg="black", font=("yu gothic ui", 17, "bold"))
        #self.sign_in_label.place(x=640, y=155)

        #full name
        self.fullname_label = Label(display_frame, text="Full name", bg="#e8bcf0", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.fullname_label.place(x=550, y=200)
        self.fullname_entry = Entry(display_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"))
        self.fullname_entry.place(x=580, y=227, width=350)

        # ===== Username icon =========
        self.username_icon = Image.open('Images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(display_frame, image=photo, bg='#e8bcf0')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=225)

        #email
        self.email_label = Label(display_frame, text="Email Address", bg="#e8bcf0", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.email_label.place(x=550, y=257)
        self.email_entry = Entry(display_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"))
        self.email_entry.place(x=580, y=284, width=350)

        self.email_icon = Image.open('Images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.email_icon)
        self.email_icon_label = Label(display_frame, image=photo, bg='#e8bcf0')
        self.email_icon_label.image = photo
        self.email_icon_label.place(x=550, y=282)

        #phonenumber
        self.number_label = Label(display_frame, text="Phone Number", bg="#e8bcf0", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.number_label.place(x=550, y=314)
        self.number_entry = Entry(display_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"))
        self.number_entry.place(x=580, y=341, width=350)

        self.number_icon = Image.open('Images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.number_icon)
        self.number_icon_label = Label(display_frame, image=photo, bg='#e8bcf0')
        self.number_icon_label.image = photo
        self.number_icon_label.place(x=550, y=339)

        #companyname
        self.comname_label = Label(display_frame, text="Company Name", bg="#e8bcf0", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.comname_label.place(x=550, y=371)
        self.comname_entry = Entry(display_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"))
        self.comname_entry.place(x=580, y=398, width=350)

        self.comname_icon = Image.open('Images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.comname_icon)
        self.comname_icon_label = Label(display_frame, image=photo, bg='#e8bcf0')
        self.comname_icon_label.image = photo
        self.comname_icon_label.place(x=550, y=396)

        #companyaddress
        self.comadd_label = Label(display_frame, text="Company Address", bg="#e8bcf0", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.comadd_label.place(x=550, y=428)
        self.comadd_entry = Entry(display_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"))
        self.comadd_entry.place(x=580, y=455, width=350)

        self.comadd_icon = Image.open('Images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.comadd_icon)
        self.comadd_icon_label = Label(display_frame, image=photo, bg='#e8bcf0')
        self.comadd_icon_label.image = photo
        self.comadd_icon_label.place(x=550, y=453)

        self.profile = Button(display_frame,text="Update Profile",command=self.profile,font=("times new roman",14, "bold"),bd=0,cursor="hand2",bg="#311432",fg="white").place(x=550,y=490,width=380)

        

    def choose(self):
        ifile = filedialog.askopenfile(parent=self.window,mode='rb',title='Choose a file')
        path = ifile.name
        self.image2 = ImageTk.PhotoImage(file=path)
        self.label.configure(image=self.image2)
        self.label.image=self.image2


    def profile(self):
        if self.fullname_entry.get()=="" or self.email_entry.get()=="" or self.number_entry.get()=="" or self.comname_entry.get()=="" or self.comadd_entry.get()=="":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)

        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
                cur = connection.cursor()
                cur.execute("select * from userregistration where user_email=%s",self.email_entry.get())
                row=cur.fetchone()

                # Check if th entered email id is already exists or not.
                if row == None:
                    messagebox.showerror("Error!","Invalid EMAIL ADDRESS",parent=self.window)
                else:
                    cur.execute("insert into clientdetail (client_name,client_email,client_number,client_companyname,client_companyaddress) values(%s,%s,%s,%s,%s)",
                                    (
                                        self.fullname_entry.get(),
                                        self.email_entry.get(),
                                        self.number_entry.get(),
                                        self.comname_entry.get(),
                                        self.comadd_entry.get(),
                                    ))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Congratulations!","Register Successful",parent=self.window)
                    #self.reset_fields()
                    # once succesfully login, direct to home page
            except Exception as es:
                messagebox.showerror("Error!",f"Error due to {es}",parent=self.window)

    #def reset_fields(self):
        #self.fullname_entry.delete(0, END)
        #self.email_entry.delete(0, END)
        #self.number_entry.delete(0, END)
        #self.comname_entry.delete(0, END)
        #self.comadd_entry.delete(0, END)
        
    def redirect_bank(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = bankstatement_page.BankStatement(root)
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
    obj = Home(root)
    root.mainloop()