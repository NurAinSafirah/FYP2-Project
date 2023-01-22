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
import numpy as np
from tkinter import font as tkfont
import cashbook_page
import home_page
import login_page
import bankstatement_page
import pandas as pd
from scipy import stats
from scipy.special import logsumexp
from sklearn.mixture import GaussianMixture
from matplotlib import pyplot as plt

class Reconcile:

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

        label_home = Label(main_frame, text="Reconciliation Page", font=("times new roman",25,"bold"),bg="#e8bcf0").place(x=20, y=5)

        self.home_button = Button(main_frame,text="Home Page",command=self.redirect_home,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=20,y=45)
        self.bank_button = Button(main_frame,text="Bank Statement",command=self.redirect_bank,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=130,y=45)
        self.cash_button = Button(main_frame,text="Cashbook Statement",command=self.redirect_cash,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=270,y=45)
        self.report_button = Button(main_frame,text="Report Summary",command=self.redirect_report,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=445,y=45)
        self.logout_button = Button(main_frame,text="Log Out",command=self.redirect_logout,font=("times new roman",13, "bold"),bd=0,cursor="hand2",bg="#e8bcf0",fg="#2c041c").place(x=1120,y=45)
        
        display_frame = Frame(self.window, bg="#e8bcf0")
        display_frame.place(x=30,y=120,width=1220,height=540)

        #bank statement
        # to read all rows availble in the table
        def bank_update(rows):
            # clearing table before showing matching search
            bank.delete(*bank.get_children())
            for i in rows:
                bank.insert('', 'end', values=i)

        def bank_getrow(event):
            rowid = bank.identify_row(event.y)
            item = bank.item(bank.focus())
            t1.set(item['values'][0])
            t2.set(item['values'][1])
            t3.set(item['values'][2])
            t4.set(item['values'][3])
            t5.set(item['values'][4])
            t6.set(item['values'][5])
            t7.set(item['values'][6])
            t8.set(item['values'][7])

        #bank statement
        # to read all rows availble in the table
        def cash_update(rows):
            # clearing table before showing matching search
            cash.delete(*cash.get_children())
            for i in rows:
                cash.insert('', 'end', values=i)

        def cash_getrow(event):
            rowid = cash.identify_row(event.y)
            item = cash.item(bank.focus())
            t1.set(item['values'][0])
            t2.set(item['values'][1])
            t3.set(item['values'][2])
            t4.set(item['values'][3])
            t5.set(item['values'][4])
            t6.set(item['values'][5])
            t7.set(item['values'][6])
            t8.set(item['values'][7])

        #RECONCILE CODE PROBLEM
        #Explanation
        #Dapatkan weightage using Expectation Maximization algorithm
        #Then that weightage should be multiply with the bank statement & cashbook statement data from MySQL database to get the score
        #Matching score formula = Weightage([varchar]reference) + Weightage([varchar]description) + Weightage([decimal]amount) +
        #                               Weightage([date]date) + Weightage([datetime]time) + Weightage(varchar]approvalcode) + Weightage([varchar]transfertype)
        #If score bank statement row A == score cashbook statement row D, It's match.
        #Match amount and unmatch amount will be calculated and a report will be generated
        def reconcile():
            if messagebox.askyesno("confirmation", "Are you want to reconcile these statements?"):
                
                data_unlabeled = pd.read_csv("test2.csv")
                x_unlabeled = data_unlabeled[["x1"]].values

                # Unsupervised learning using EM Algorithm for weightage
                print("unsupervised: ")
                random_params = initialize_random_params()
                #weightage_get = run_em(x_unlabeled, random_params)
                #weightage = np.array(weightage_get)
                #print(weightage)
                #weightage = [[0.0], [0.6], [0.7], [0.4], [0.5], [0.3], [0.8], [0.7]]
                #print(run_em(x_unlabeled, random_params))
                weightage = [[run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)], [run_em(x_unlabeled, random_params)]]
                
                #bank statement
                self.cursor.execute("select * from bankstatementstorage")
                bank_row = self.cursor.fetchall()
                y = np.array(bank_row)
                y.shape
                bank_table = np.reshape(y, (-1,8,1))
                print("Get all transaction in bank statement")
                
                for bank_data in bank_table:
                    for weight_row in weightage:
                    # Attempt to change bank data from string to binary
                        #bank_data = np.asfarray(bank_data)
                        #bank_data = y.join(format(i, '08b') for i in bytearray(bank_data, encoding ='utf-8'))
                        #if not isinstance(bank_data, int):
                            #'bank_data'.encode('ascii')
                        display_scorebank = np.concatenate((bank_data, weightage), axis=1)
                    # ERROR - cannot multiply string with float
                    #score = bank_data * weightage
                    print(display_scorebank)
                    print(score)
                    #print("\n")

                #cash statement
                self.cursor.execute("select * from cashbookstorage")
                cash_row = self.cursor.fetchall()
                y = np.array(cash_row)
                y.shape
                cash_table = np.reshape(y, (-1,8,1))
                #print(bank_table)
                print("Get all transaction in cash statement")
                for cash_data in cash_table:
                    for weight_row in weightage:
                        display_scorecash = np.concatenate((cash_data, weightage), axis=1)
                    #score = float(bank_data) * weightage
                    #try masukkan calculation recon kat sini
                    #print(display_scorecash)
                    #print(score)
                    #print("\n")
                    
                #The match between both statements should be based on matching score but
                #Since still cannot multiply with the weightage, we try to find the match first
                print("\nReconcile Summary")
                reconcile_count = 0
                match_amount = 0
                total_amount = 0
                unmatch_amount = 0
                sheet1 = 0
                sheet3 = 0

                while sheet1 < len(bank_table):
                    sheet2 = 0
                    while sheet2 < len(cash_table):
                        if bank_table[sheet1][6] == cash_table[sheet2][6]:
                            reconcile_count = reconcile_count + 1
                            print("\nCounter of matched data: " + str(reconcile_count))
                            match_amount = match_amount + bank_table[sheet1][3]
                            print("Total Match Amount: " + str(match_amount) + "\n")
                            pager = 1
                            while pager < 3:
                                count = 0
                                #use this if want to print the data one by one (row and column), meaning you read data as one row and its column one by one
                                # if pager%2 != 0:
                                #    print("Bank statement :")
                                #    while count < 8:
                                #        print(bank_table[sheet1][count])
                                #        count = count + 1
                                # if pager%2 == 0:
                                #    print("Cashbook :")
                                #    while count < 8:
                                #        print(cash_table[sheet2][count])
                                #        count = count + 1
                                #use this if want to print the data straight away (row), meaning you read data as one row straight away
                                if pager%2 != 0:
                                    print("Bank statement :")
                                    print(bank_table[sheet1])
                                if pager%2 == 0:
                                    print("Cashbook :")
                                    print(cash_table[sheet2])
                                pager = pager + 1   
                        sheet2 = sheet2 + 1
                    else:
                        total_amount = total_amount + bank_table[sheet1][3]
                        unmatch_amount = total_amount - match_amount
                    sheet1 = sheet1 + 1
                
                print("\nTotal Match Amount: RM" + str(match_amount))
                print("Total Unmatch Amount: RM" + str(unmatch_amount) + "\n") 

                # Attempt to convert string to binary
                # #score = bin(cash_data)
                # #display = np.concatenate((display_scorebank,display_scorecash), axis=1)
                # #z = map(bin,bytearray(cash_data))
                # #print(list(z))

                messagebox.showinfo("Successful", "Reconcile is done")
            else:
                messagebox.showinfo("Warning", "Reconcile is cancelled")

        def match():
            END

        #Algorithm EM
        def get_random_psd(n):
            x = np.random.normal(0, 1, size=(n, n))
            return np.dot(x, x.transpose())


        def initialize_random_params():
            params = {'phi': np.random.uniform(0, 1),
                    'mu0': np.random.normal(0, 1, size=(2,)),
                    'mu1': np.random.normal(0, 1, size=(2,)),
                    'sigma0': get_random_psd(2),
                    'sigma1': get_random_psd(2)}
            return params


        def learn_params(x_labeled, y_labeled):
            n = x_labeled.shape[0]
            phi = x_labeled[y_labeled == 1].shape[0] / n
            mu0 = np.sum(x_labeled[y_labeled == 0], axis=0) / x_labeled[y_labeled == 0].shape[0]
            mu1 = np.sum(x_labeled[y_labeled == 1], axis=0) / x_labeled[y_labeled == 1].shape[0]
            sigma0 = np.cov(x_labeled[y_labeled == 0].T, bias= True)
            sigma1 = np.cov(x_labeled[y_labeled == 1].T, bias=True)
            return {'phi': phi, 'mu0': mu0, 'mu1': mu1, 'sigma0': sigma0, 'sigma1': sigma1}


        def e_step(x, params):
            np.log([stats.multivariate_normal(params["mu0"], params["sigma0"]).pdf(x),
                    stats.multivariate_normal(params["mu1"], params["sigma1"]).pdf(x)])
            log_p_y_x = np.log([1-params["phi"], params["phi"]])[np.newaxis, ...] + \
                        np.log([stats.multivariate_normal(params["mu0"], params["sigma0"]).pdf(x),
                    stats.multivariate_normal(params["mu1"], params["sigma1"]).pdf(x)]).T
            log_p_y_x_norm = logsumexp(log_p_y_x, axis=1)
            return log_p_y_x_norm, np.exp(log_p_y_x - log_p_y_x_norm[..., np.newaxis])


        def m_step(x, params):
            total_count = x.shape[0]
            _, heuristics = e_step(x, params)
            heuristic0 = heuristics[:, 0]
            heuristic1 = heuristics[:, 1]
            sum_heuristic1 = np.sum(heuristic1)
            sum_heuristic0 = np.sum(heuristic0)
            phi = (sum_heuristic1/total_count)
            mu0 = (heuristic0[..., np.newaxis].T.dot(x)/sum_heuristic0).flatten()
            mu1 = (heuristic1[..., np.newaxis].T.dot(x)/sum_heuristic1).flatten()
            diff0 = x - mu0
            sigma0 = diff0.T.dot(diff0 * heuristic0[..., np.newaxis]) / sum_heuristic0
            diff1 = x - mu1
            sigma1 = diff1.T.dot(diff1 * heuristic1[..., np.newaxis]) / sum_heuristic1
            params = {'phi': phi, 'mu0': mu0, 'mu1': mu1, 'sigma0': sigma0, 'sigma1': sigma1}
            return params


        def get_avg_log_likelihood(x, params):
            loglikelihood, _ = e_step(x, params)
            return np.mean(loglikelihood)


        def run_em(x, params):
            avg_loglikelihoods = []
            while True:
                avg_loglikelihood = get_avg_log_likelihood(x, params)
                avg_loglikelihoods.append(avg_loglikelihood)
                if len(avg_loglikelihoods) > 2 and abs(avg_loglikelihoods[-1] - avg_loglikelihoods[-2]) < 0.0001:
                    break
                params = m_step(x_unlabeled, params)
            print((params['phi']))
            _, posterior = e_step(x_unlabeled, params)
            forecasts = np.argmax(posterior, axis=1)
            #return forecasts, posterior, avg_loglikelihoods
            return params['phi']

        if __name__ == '__main__':
            data_unlabeled = pd.read_csv("test2.csv")
            x_unlabeled = data_unlabeled[["x1"]].values

        #declare
        t1 = StringVar()
        t2 = StringVar()
        t3 = StringVar()
        t4 = StringVar()
        t5 = StringVar()
        t6 = StringVar()
        t7 = StringVar()
        t8 = StringVar()

        self.connection = mysql.connector.connect(host="localhost", user="root", password="Ainsafirah97!", database="fyp")
        self.cursor = self.connection.cursor()
            

        # divide the frame into multiples section with seperation and title
        wrapper1 = LabelFrame(display_frame, text="Bank Statement", bg="#e8bcf0")
        wrapper2 = LabelFrame(display_frame, text="Cashbook Statement", bg="#e8bcf0")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        # for bank statement Section
        bank = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6,7,8), show="headings", height="8")
        bank.pack()

        bank.heading(1, text="ID")
        bank.column(1, anchor=CENTER, stretch=NO, width=50)
        bank.heading(2, text="Reference")
        bank.column(2, anchor=CENTER, stretch=NO, width=140)
        bank.heading(3, text="Description")
        bank.column(3, anchor=CENTER, stretch=NO, width=140)
        bank.heading(4, text="Amount")
        bank.column(4, anchor=CENTER, stretch=NO, width=110)
        bank.heading(5, text="Date")
        bank.column(5, anchor=CENTER, stretch=NO, width=110)
        bank.heading(6, text="Time")
        bank.column(6, anchor=CENTER, stretch=NO, width=110)
        bank.heading(7, text="Approval Code")
        bank.column(7, anchor=CENTER, stretch=NO, width=140)
        bank.heading(8, text="Transfer Type")
        bank.column(8, anchor=CENTER, stretch=NO, width=140)

        bank.bind('<Double 1>', bank_getrow)
        query = "select * from bankstatementstorage"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        bank_update(rows)

        # for bank statement Section
        cash = ttk.Treeview(wrapper2, columns=(1,2,3,4,5,6,7,8), show="headings", height="8")
        cash.pack()

        cash.heading(1, text="ID")
        cash.column(1, anchor=CENTER, stretch=NO, width=50)
        cash.heading(2, text="Reference")
        cash.column(2, anchor=CENTER, stretch=NO, width=140)
        cash.heading(3, text="Description")
        cash.column(3, anchor=CENTER, stretch=NO, width=140)
        cash.heading(4, text="Amount")
        cash.column(4, anchor=CENTER, stretch=NO, width=110)
        cash.heading(5, text="Date")
        cash.column(5, anchor=CENTER, stretch=NO, width=110)
        cash.heading(6, text="Time")
        cash.column(6, anchor=CENTER, stretch=NO, width=110)
        cash.heading(7, text="Approval Code")
        cash.column(7, anchor=CENTER, stretch=NO, width=140)
        cash.heading(8, text="Transfer Type")
        cash.column(8, anchor=CENTER, stretch=NO, width=140)

        cash.bind('<Double 1>', cash_getrow)
        query = "select * from cashbookstorage"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        cash_update(rows)

    #command reconcile
        reconcilebutton = Button(display_frame, text="Reconcile", command=reconcile)
        reconcilebutton.pack(side=tk.LEFT, padx=20, pady=10)


    def redirect_home(self):
        #self.window.destroy()
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
    obj = Reconcile(root)
    root.mainloop()
