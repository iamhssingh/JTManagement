from functools import partial
from tkinter import messagebox
from tkinter.tix import *

import compo.dbactions as actions
import compo.transactions as transactions


cid = []
cname = []
cmnumber = []


# mainbg = "SlateBlue2"
# outerbg = "Red"
# windowbg = "Yellow"
# buttonbg = "Blue"


def addbutton(row, col, master, text, imagez=None, command=None):
    if command is not None and imagez is not None:
        x = Button(master=master, text=text, image=imagez, command=command)
        x.image = imagez
    elif command is not None and imagez is None:
        x = Button(master=master, text=text, command=command)
    elif imagez is not None and command is None:
        x = Button(master=master, text=text, image=imagez)
        x.image = imagez
    else:
        x = Button(master=master, text=text)
    x.grid(row=row, column=col)
    return x


def addlabel(master, text, row, column):
    cname_label = Label(master=master, text=text)
    cname_label.grid(row=row, column=column)
    return cname_label


def addentry(master, textvar, row, column):
    new_entry = Entry(master=master, textvariable=textvar)
    new_entry.grid(row=row, column=column)
    return new_entry


def getcustomer(frame, uid):
    del cid[:]
    del cmnumber[:]
    del cname[:]
    customers = actions.getcustomers(uid)
    cstmr_button = []
    for cstmr in range(0, len(customers)):
        cid.append(customers[cstmr][2])
        cname.append(customers[cstmr][0])
        cmnumber.append(customers[cstmr][1])
        cstmr_button.append(Button(master=frame, text=cname[cstmr], command=partial(transactions.showtransactions,
                                                                                    customers[cstmr][2], cid, cname)))
    return cstmr_button


def loggedin(uid, fname, lname):
    def confirm():
        if messagebox.askyesno("Quit", "Do you really wish to quit?"):
            os.popen("copy media\maindb.db %APPDATA%\JTManagement\maindb_backup.db".format(fname + "_" + lname))
            workwindow.destroy()

    workwindow = Tk()
    #     workwindow.iconbitmap("media/images/am.ico")
    banner_image = PhotoImage(file="media/images/jt.gif")
    export_image = PhotoImage(file="media/images/export.gif")

    astatus = IntVar()
    w, h = workwindow.winfo_screenwidth(), workwindow.winfo_screenheight()
    workwindow.geometry('{}x{}+0+0'.format(w - 20, h - 80))
    workwindow.title("Account Manager for {}".format(fname + " " + lname))
    workwindow.protocol("WM_DELETE_WINDOW", confirm)

    def refresh():

        def remove():
            anc_button.destroy()
            bckup.destroy()
            addnewcustomer()

        def export_cstmr(c_id, name):
            r = actions.gettransactions(c_id)
            header = [('Customer ID', 'Item', 'Item Price', 'Quantity', 'Total Price', 'Payment Done', 'Dues Remaining',
                       'Buy Date', 'Entry Date')]
            c = transactions.filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('Excel Files', '.csv')],
                                                          initialfile='{}'.format(name),
                                                          title="Choose your Excel File", initialdir="/", parent=win)
            file = open(c, 'w', newline='', encoding='utf8')
            wr = transactions.csv.writer(file)
            wr.writerows(header)
            wr.writerows(r)

        def backup():
            c = transactions.filedialog.asksaveasfilename(defaultextension='.db', filetypes=[('Database File', '.db')],
                                                          initialfile='{}'.format(fname + "_" + lname),
                                                          title="Choose your Backup Location", initialdir="\ ",
                                                          parent=win)
            a = ''
            for m in range(0, len(c)):
                if c[m] == "/":
                    a = a + '\\'
                else:
                    a = a + c[m]
            print(a)
            os.popen("copy media\maindb.db " + a)

        getcstmr = getcustomer(win, uid)
        addlabel(win, "{} customers found!".format(len(getcstmr)), 1, 0)
        addlabel(win, "Customer Name(Click on button)", 2, 0)
        addlabel(win, "                       ", 2, 1)
        addlabel(win, "                       ", 2, 2)
        addlabel(win, "Customer Mobile Numbers", 2, 3)
        x = 3
        for z in range(0, len(getcstmr)):
            getcstmr[z].grid(row=x + z, column=0)
            addlabel(win, cmnumber[z], x + z, 3)
            addbutton(x + z, 7, win, 'Export', export_image, partial(export_cstmr, cid[z], cname[z]))

        anc_button = Button(master=win, padx=4, pady=4, text="Add New Customer", image=addcustomer_image,
                            bg='cornflower blue', command=remove)
        anc_button.image = addcustomer_image
        anc_button.grid(row=x + len(getcstmr) + 1, column=0)

        bckup = Button(master=win, padx=4, pady=4, text="Backup Database", command=backup)
        bckup.grid(row=x + len(getcstmr) + 1, column=3)

    def addnewcustomer():
        def cnfrm():
            if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
                refresh()
                addnewcustomer_window.destroy()

        addnewcustomer_window = Toplevel()
        cname_var = StringVar()
        cmnumber_var = IntVar()
        addnewcustomer_window.geometry('350x150+600+250')
        addnewcustomer_window.title("Add new customer")
        addnewcustomer_window.protocol("WM_DELETE_WINDOW", cnfrm)

        def add():
            x = cname_var.get()
            y = cmnumber_var.get()
            if len(x) > 0 and len(str(y)) == 10:
                astatus.set(actions.addcustomer(uid, x, y))
                if astatus.get() == 1:
                    refresh()
                    addnewcustomer_window.destroy()
            else:
                messagebox.showwarning(title="Invalid Entry!",
                                       message="All fields are required! and Mobile Number can only be 10 digit long!")
                addnewcustomer_window.destroy()
                addnewcustomer()

        addlabel(addnewcustomer_window, "Customer Name: ", 1, 0)
        addentry(addnewcustomer_window, cname_var, 1, 3)

        addlabel(addnewcustomer_window, "Customer Mobile Number: ", 3, 0)
        addentry(addnewcustomer_window, cmnumber_var, 3, 3)

        add_button = Button(master=addnewcustomer_window, text="Add Now", image=addnow_image, bg='forest green',
                            command=add)
        add_button.image = addnow_image
        add_button.grid(row=5, column=3)

        addnewcustomer_window.mainloop()

    welcomelabel = Label(workwindow, text="Welcome Mr. {}".format(fname + " " + lname))
    welcomelabel.pack()
    Label(workwindow, image=banner_image).pack(fill=X, expand=1)

    swin = ScrolledWindow(workwindow, width=w - 80, height=h - 200)
    swin.pack(fill=X, expand=1)
    win = swin.window

    addcustomer_image = PhotoImage(file="media/images/addcustomer.gif")
    addnow_image = PhotoImage(file="media/images/addnow.gif")

    refresh()

    workwindow.mainloop()
