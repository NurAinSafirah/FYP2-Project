from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql
import os
from home_page import *
import credentials as cr
import home_page
import signup_page
from signup_page import *

class Login:
    def __init__(self, root):
        self.window = root
        self.window.title("Bank Reconciliation")
        # Set the window size
        # Here 0,0 represents the starting point of the window 
        self.window.geometry("1080x600+115+70")
        self.window.config(bg = "#7600bc")

        #============================================================================
        #==============================DESIGN PART===================================
        #============================================================================

        self.bg_img = ImageTk.PhotoImage(file="Images/3.jpg")
        backgroundpic = Label(self.window,image=self.bg_img).place(x=0,y=0)

        frame = Frame(self.window, bg="#e8bcf0", highlightbackground="#710193", highlightthickness=1)
        frame.place(x=420,y=90,width=460,height=550)

        self.window.state('zoomed')

        #self.frame1 = Frame(self.window, bg="#7600bc")
        #self.frame1.place(x=0, y=0, width=400, relheight = 1)

        label1 = Label(frame, text= "     Automated Bank", font=("times new roman", 30, "bold"), bg="#e8bcf0", fg="black").place(x=30,y=20)
        label2 = Label(frame, text= "Reconciliation Sofware", font=("times new roman", 30, "bold"), bg="#e8bcf0", fg="black").place(x=30,y=70)

        #=============Entry Field & Buttons============

        #self.frame2 = Frame(self.window, bg = "#e8bcf0")
        #self.frame2.place(x=450,y=0,relwidth=1, relheight=1)

        #self.frame3 = Frame(self.frame2, bg="#e8bcf0")
        #self.frame3.place(x=140,y=150,width=500,height=450)

        self.email_label = Label(frame,text="Email Address", font=("times new roman",20,"bold"),bg="#e8bcf0", fg="black").place(x=30,y=180)
        self.email_entry = Entry(frame,font=("roboto",15),bg="white",fg="black")
        self.email_entry.place(x=30, y=220, width=400)

        self.password_label = Label(frame,text="Password", font=("times new roman",20,"bold"),bg="#e8bcf0", fg="black").place(x=30,y=270)
        self.password_entry = Entry(frame,font=("robotp",15),bg="white",fg="black",show="*")
        self.password_entry.place(x=30, y=310, width=400)

        #================Buttons===================
        self.login_button = Button(frame,text="Log In",command=self.login_func,font=("times new roman",15, "bold"),bd=0,cursor="hand2",bg="#311432",fg="white").place(x=30,y=380,width=400)

        self.forgotten_pass = Button(frame,text="Forgotten Password?",command=self.forgot_func,font=("times new roman",10, "bold", "underline"),bd=0,cursor="hand2",bg="#e8bcf0",fg="blue3").place(x=157,y=430,width=150)

        self.create_button = Button(frame,text="Create New Account",command=self.redirect_window,font=("times new roman",10, "bold", "underline"),bd=0,cursor="hand2",bg="#e8bcf0",fg="blue3").place(x=157,y=450,width=150)


    def login_func(self):
        if self.email_entry.get()=="" or self.password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required",parent=self.window)
        else:
            try:
                connection=pymysql.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
                cur = connection.cursor()
                cur.execute("select * from userregistration where user_email=%s and user_password=%s",(self.email_entry.get(),self.password_entry.get()))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error!","Invalid USERNAME & PASSWORD",parent=self.window)
                else:
                    #messagebox.showinfo("Success","Welcome to the Bank Reconciliation Software",parent=self.window)
                    # Clear all the entries
                    #self.reset_fields()
                    # once succesfully login, direct to home page
                    self.redirect_homepage()
                    
                    connection.close()

            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    def forgot_func(self):
        if self.email_entry.get()=="":
            messagebox.showerror("Error!", "Please enter your Email Id",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
                cur = connection.cursor()
                cur.execute("select * from userregistration where user_email=%s", self.email_entry.get())
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error!", "Email Id doesn't exists")
                else:
                    connection.close()
                    
                    #=========================SECOND WINDOW===============================
                    #------------Toplevel:create a window top of another window-----------
                    #------------focus_force:Helps to to focus on the current window------
                    #-----Grab:Helps to grab the current window until user ungrab it------

                    self.root=Toplevel()
                    self.root.title("Forget Password?")
                    self.root.geometry("400x440+450+200")
                    self.root.config(bg="white")
                    self.root.focus_force()
                    self.root.grab_set()

                    title3 = Label(self.root,text="Change your password",font=("times new roman",20,"bold"),bg="white").place(x=10,y=10)

                    title4 = Label(self.root,text="It's quick and easy",font=("times new roman",12),bg="white").place(x=10,y=45)

                    title5 = Label(self.root, text="Select your question", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=85)

                    self.sec_ques = ttk.Combobox(self.root,font=("times new roman",13),state='readonly',justify=CENTER)
                    self.sec_ques['values'] = ("Select","What's your pet name?","Your first teacher name","Your birthplace", "Your favorite movie")
                    self.sec_ques.place(x=10,y=120, width=270)
                    self.sec_ques.current(0)
                    
                    title6 = Label(self.root, text="Answer", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=160)

                    self.ans = Entry(self.root,font=("arial"))
                    self.ans.place(x=10,y=195,width=270)

                    title7 = Label(self.root, text="New Password", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=235)

                    self.new_pass = Entry(self.root,font=("arial"))
                    self.new_pass.place(x=10,y=270,width=270)

                    self.create_button = Button(self.root,text="Submit",command=self.change_pass,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="blue3",fg="white").place(x=95,y=340,width=200)
                    #=========================================================================

            except Exception as e:
                messagebox.showerror("Error", f"{e}")
                
      
    def change_pass(self):
        if self.email_entry.get() == "" or self.sec_ques.get() == "Select" or self.new_pass.get() == "":
            messagebox.showerror("Error!", "Please fill the all entry field correctly")
        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
                cur = connection.cursor()
                cur.execute("select * from userregistration where user_email=%s and user_question=%s and user_answer=%s", (self.email_entry.get(),self.sec_ques.get(),self.ans.get()))
                row=cur.fetchone()

                if row == None:
                    messagebox.showerror("Error!", "Please fill the all entry field correctly")
                else:
                    try:
                        cur.execute("update userregistration set user_password=%s where user_email=%s", (self.new_pass.get(),self.email_entry.get()))
                        connection.commit()

                        messagebox.showinfo("Successful", "Password has changed successfully")
                        connection.close()
                        self.reset_fields()
                        self.root.destroy()

                    except Exception as er:
                        messagebox.showerror("Error!", f"{er}")
                        
            except Exception as er:
                        messagebox.showerror("Error!", f"{er}")
            

    def redirect_window(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the sign up window
        obj = signup_page.SignUp(root)
        root.mainloop()

    #
    def redirect_homepage(self):
        self.window.destroy()
        # The page must be in the same directory
        root = Tk()
        # Importing the home window
        obj = home_page.Home(root)
        root.mainloop()

    def reset_fields(self):
        self.email_entry.delete(0,END)
        self.password_entry.delete(0,END)

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
