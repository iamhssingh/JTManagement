__author__ = 'iamhssingh'

import sqlite3
from tkinter import messagebox

try:
    db = sqlite3.connect("bmngmnt.db")
    c = db.cursor()
except sqlite3.Error as err:
    messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))


def register(un, ufn, uln, up, ucp):
    import datetime

    if up == ucp:
        signup = ("INSERT INTO user_master (userName, userFName, userLName, userPassword) VALUES (?, ?, ?, ?)")
        data = (un, ufn, uln, up)
        try:
            c.execute(signup, data)
            db.commit()
            messagebox.showinfo(title="ID Created", message="Registration Successful. Please save data somewhere safe!")
            return 1
        except sqlite3.Error as err:
            messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))
            return 0

    else:
        messagebox.showwarning(title="Wrong Password", message="Password not confirmed!")
        return 0


def login(username, userpassword):
    try:
        c.execute(
            "SELECT userPassword, userFName, userLName, userID FROM user_master WHERE userName =?",
            (username,))
        data = c.fetchall()
        if len(data) > 0:
            for row in data:
                dbuPassword = row[0]
                dbuFName = row[1]
                dbuLName = row[2]
                dbuID = row[3]
            if userpassword == dbuPassword:
                messagebox.showinfo(title="Success", message="Welcome {}".format(dbuFName + " " + dbuLName))
                return dbuID, dbuFName, dbuLName, dm
            elif userpassword != dbuPassword:
                messagebox.showwarning(title="Invalid Password", message="Sorry! Password you entered is not correct!")
                return 0
        else:
            messagebox.showwarning(title="Invalid UserName", message="{} username does not exist!".format(username))
            return 0
    except sqlite3.Error as err:
        messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))


def getcustomers(dbuID):
    try:
        c.execute("SELECT customerName, customerMobileNumber, customerID FROM customers_master WHERE userID =?",
                  (dbuID,))
        data = c.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))


def addcustomer(uid, cn, cmn):
    try:
        add = ("INSERT INTO customers_master"
               "(userID, customerName, customerMobileNumber)"
               "VALUES (?, ?, ?)")
        data = (uid, cn, cmn)
        c.execute(add, data)
        db.commit()
        messagebox.showinfo(title="Added", message="{} added successfully to your customer list!".format(cn))
        return 1
    except sqlite3.Error as err:
        messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))


def gettransactions(dbcID):
    try:
        c.execute(
            "SELECT transactionID, item, itemprice, qty, totalprice, payment, dues, customerDues, paiddate, entrydate FROM transaction_master WHERE customerID =?",
            (dbcID,))
        data = c.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))


def addtransaction(dbcID, dbitem, dbitemprice, dbqty, dbtprice, dbpay, dbdues, dbtdues, dbbdate, dbedate):
    try:
        add = ("INSERT INTO transaction_master"
               "(customerID, item, itemprice, qty, totalprice, payment, dues, customerDues, paiddate, entrydate)"
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        data = (dbcID, dbitem, dbitemprice, dbqty, dbtprice, dbpay, dbdues, dbtdues, dbbdate, dbedate)
        c.execute(add, data)
        db.commit()
        return 1
    except sqlite3.Error as err:
        messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))
