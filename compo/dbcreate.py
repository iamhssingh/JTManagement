__author__ = 'iamhssingh'

import sqlite3
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox

root = Tk()

c = filedialog.asksaveasfilename(defaultextension='.db', filetypes=[('database files', '.db')], initialfile='bmngmnt',
                                 title="Choose your databasefile", initialdir="/", parent=root)

success = False
create = False
try:
    db = sqlite3.connect(c)
    cursor = db.cursor()
    success = True
except sqlite3.Error as err:
    messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))

if success == True:
    try:
        cursor.execute("""CREATE TABLE `user_master` (
	`userID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`userName`	TEXT NOT NULL,
	`userFName`	TEXT NOT NULL,
	`userLName`	TEXT NOT NULL,
	`userPassword`	TEXT NOT NULL,
	`userSecurityQ1`	TEXT NOT NULL,
	`userSecurityQ2`	TEXT NOT NULL,
	`userSecurityA1`	TEXT NOT NULL,
	`userSecurityA2`	TEXT NOT NULL,
	`userCreateDate`	TEXT NOT NULL
);""")
        print("Created USER master")

        cursor.execute("""CREATE TABLE `customers_master` (
	`customerID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`userID`	INTEGER NOT NULL,
	`customerName`	TEXT NOT NULL,
	`customerMobileNumber`	TEXT NOT NULL
);""")
        print("Created customers master")

        cursor.execute("""CREATE TABLE `transaction_master` (
  `transactionID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  `customerID`	INTEGER NOT NULL,
  `customerDues`	INTEGER NOT NULL,
  `item`	TEXT NOT NULL,
  `itemprice`	REAL NOT NULL,
  `qty`	REAL NOT NULL,
  `totalprice`	REAL NOT NULL,
  `payment`	REAL NOT NULL,
  `dues`	REAL NOT NULL,
  `paiddate`	TEXT NOT NULL,
  `entrydate`	TEXT NOT NULL);""")
        print("Created Transaction master")
        create = True
    except sqlite3.Error as err:
        messagebox.showwarning(title="Database Connection Error", message="Something went wrong: {}".format(err))

if create == True and success == True:
    print("All Job Done")
    filedata = None
    with open('compo/dbactions.py', 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace("file = ''", "file = '{}' ".format(c))
    filedata = filedata.replace('table_db_create = False', "table_db_create = True")
    # Write the file out again
    with open('compo/dbactions.py', 'w') as file:
        file.write(filedata)

root.destroy()
