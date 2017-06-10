__author__ = 'iamhssingh'

import csv
import datetime
from functools import partial
from tkinter import filedialog
from tkinter import messagebox
from tkinter.tix import *

from compo import dbactions

today = datetime.datetime.now()

lstatus = []

tid = []
titem = []
tprice = []
tqty = []
ttprice = []
tpay = []
tdues = []
tbdate = []
tedate = []
ttdues = []
header = [('Customer ID', 'Item', 'Item Price', 'Quantity', 'Total Price', 'Payment Done', 'Dues Remaining',
           'Total Dues', 'Buy Date', 'Entry Date')]


def addButton(row, col, master, text, imagez=None, command=None):
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


def addLabel(master, text, row, column):
    cname_label = Label(master=master, text=text)
    cname_label.grid(row=row, column=column)
    return cname_label


def addEntry(master, textvar, row, column):
    new_entry = Entry(master=master, textvariable=textvar)
    new_entry.grid(row=row, column=column)
    return new_entry


def gettrans(cstmrid):
    del tid[:]
    del titem[:]
    del tprice[:]
    del tqty[:]
    del ttprice[:]
    del tpay[:]
    del tdues[:]
    del ttdues[:]
    del tbdate[:]
    del tedate[:]

    transactions1 = dbactions.gettransactions(cstmrid)

    transactions = []
    for row in range(0, len(transactions1)):
        transactions.append(list(transactions1[row]))

    for row in range(0, len(transactions)):
        transactions[row][0] = int(row)
        tid.append(transactions[row][0])
        titem.append(transactions[row][1])
        tprice.append(float(transactions[row][2]))
        tqty.append(transactions[row][3])
        ttprice.append(float(transactions[row][4]))
        tpay.append(float(transactions[row][5]))
        tdues.append(float(transactions[row][6]))
        ttdues.append(float(transactions[row][7]))
        tbdate.append(str(transactions[row][8]))
        tedate.append(str(transactions[row][9]))
    return transactions


def showtransactions(cstmrid, lcid, lcname):
    def tconfirm():
        if messagebox.askyesno(parent=twin, title="Quit", message="Do you really wish to quit?"):
            tranwindow.destroy()

    def export_csv(data):
        c = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('Excel Files', '.csv')],
                                         initialfile='{}'.format(lcname[cindex]), title="Choose your Excel File",
                                         initialdir="/", parent=tranwindow)
        file = open(c, 'w', newline='', encoding='utf8')
        wr = csv.writer(file)
        wr.writerows(header)
        wr.writerows(data)

    tranwindow = Toplevel()
    cindex = lcid.index(cstmrid)
    #     tranwindow.iconbitmap("media/images/am.ico")

    addnew_image = PhotoImage(file="media/images/addnew.gif")
    load_image = PhotoImage(file="media/images/load.gif")
    date_image = PhotoImage(file="media/images/date.gif")
    export_image = PhotoImage(file="media/images/export.gif")

    w, h = tranwindow.winfo_screenwidth(), tranwindow.winfo_screenheight()
    tranwindow.geometry('{}x{}+0+0'.format(w - 20, h - 80))
    tranwindow.title("Transactions Detail for {}".format(lcname[cindex]))
    tranwindow.protocol("WM_DELETE_WINDOW", tconfirm)

    atstatus = IntVar()
    itemvar = StringVar()
    pricevar = DoubleVar()
    qtyvar = DoubleVar()
    tpricevar = DoubleVar()
    payvar = DoubleVar()
    duesvar = DoubleVar()
    bdatevar = StringVar()
    tduesvar = StringVar()

    edatevar = StringVar()
    now = datetime.datetime.now()
    f = '%Y-%m-%d %H:%M:%S'
    edatevar.set(now.strftime(f))

    def refresh_t():
        edatevar = StringVar()
        now = datetime.datetime.now()
        f = '%Y-%m-%d %H:%M:%S'
        edatevar.set(now.strftime(f))

        itemvar.set('')
        pricevar.set(0)
        qtyvar.set(0)
        tpricevar.set(0)
        payvar.set(0)
        duesvar.set(0)
        tduesvar.set(0)
        bdatevar.set(0)

        def bdateset():
            bdateset_win = Toplevel()
            bdateset_win.title("Set Buy Date")

            addLabel(bdateset_win, 'DATE: ', 0, 0)
            addLabel(bdateset_win, 'MONTH: ', 0, 2)
            addLabel(bdateset_win, 'YEAR: ', 0, 4)
            addLabel(bdateset_win, 'HOUR: ', 0, 6)
            addLabel(bdateset_win, 'MINUTE: ', 0, 8)
            d = Spinbox(bdateset_win, from_=1, to=31)
            d.grid(row=1, column=0)
            m = Spinbox(bdateset_win, from_=1, to=12)
            m.grid(row=1, column=2)
            y = Spinbox(bdateset_win, from_=2000, to=2100)
            y.grid(row=1, column=4)
            h = Spinbox(bdateset_win, from_=0, to=23)
            h.grid(row=1, column=6)
            mi = Spinbox(bdateset_win, from_=0, to=59)
            mi.grid(row=1, column=8)
            s = '0'

            submit_image = PhotoImage(file="media/images/submit.gif")

            def convert(today=False):
                if today is True:
                    date = datetime.datetime(int(now.strftime('%Y')), int(now.strftime('%m')), int(now.strftime('%d')),
                                             int(now.strftime('%H')), int(now.strftime('%M')))
                if today is False:
                    date = datetime.datetime(int(y.get()), int(m.get()), int(d.get()), int(h.get()), int(mi.get()),
                                             int(s))
                bdatevar.set(date)
                addLabel(twin, bdatevar.get(), z, 16)
                bdateset_win.destroy()

            addLabel(bdateset_win, "                      ", 2, 8)
            addButton(3, 8, bdateset_win, 'SUBMIT', submit_image, convert)
            addButton(3, 6, bdateset_win, 'TODAY', command=partial(convert, True))

        def addt(i, p, q, ub, pa, du, bdst, ed, export):
            i.destroy()
            p.destroy()
            q.destroy()
            ub.destroy()
            pa.destroy()
            du.destroy()
            bdst.destroy()
            ed.destroy()
            export.destroy()
            if len(itemvar.get()) > 0:
                atstatus.set(
                    dbactions.addtransaction(cstmrid, itemvar.get(), pricevar.get(), qtyvar.get(), tpricevar.get(),
                                             payvar.get(), duesvar.get(), tduesvar.get(), bdatevar.get(),
                                             edatevar.get()))
                refresh_t()
            else:
                messagebox.showwarning(title="Empty Transaction",
                                       message="Transaction has no buy date and name! Please specify Buy Date and Item Name!")
                tranwindow.destroy()
            if atstatus.get() == 1:
                messagebox.showinfo(parent=twin, title="Adding Succesful", message="1 transaction added successfully")

        total = gettrans(cstmrid)
        addLabel(twin, "{} transactions found!".format(len(tid)), 0, 0)
        addLabel(twin, "Transaction ID", 2, 0)
        addLabel(twin, "|||", 2, 1)
        addLabel(twin, "Item", 2, 2)
        addLabel(twin, "|", 2, 3)
        addLabel(twin, "Item Price(Cost per Item)", 2, 4)
        addLabel(twin, "||", 2, 5)
        addLabel(twin, "Quantity", 2, 6)
        addLabel(twin, "|", 2, 7)
        addLabel(twin, "Total Price(Item Price * Quantity)", 2, 8)
        addLabel(twin, "||", 2, 9)
        addLabel(twin, "Payment", 2, 10)
        addLabel(twin, "|", 2, 11)
        addLabel(twin, "Dues", 2, 12)
        addLabel(twin, "|", 2, 13)
        addLabel(twin, "Total Dues", 2, 14)
        addLabel(twin, "||", 2, 15)
        addLabel(twin, "Buy Date", 2, 16)
        addLabel(twin, "|", 2, 17)
        addLabel(twin, "Entry Date", 2, 18)

        x = 3
        z = x + len(tid)

        for trans in range(0, len(tid)):
            addLabel(twin, trans, x + trans, 0)
            addLabel(twin, "|||", x + trans, 1)
            addLabel(twin, titem[trans], x + trans, 2)
            addLabel(twin, "|", x + trans, 3)
            addLabel(twin, tprice[trans], x + trans, 4)
            addLabel(twin, "||", x + trans, 5)
            addLabel(twin, tqty[trans], x + trans, 6)
            addLabel(twin, "|", x + trans, 7)
            addLabel(twin, ttprice[trans], x + trans, 8)
            addLabel(twin, "||", x + trans, 9)
            addLabel(twin, tpay[trans], x + trans, 10)
            addLabel(twin, "|", x + trans, 11)
            addLabel(twin, tdues[trans], x + trans, 12)
            addLabel(twin, "|", x + trans, 13)
            addLabel(twin, ttdues[trans], x + trans, 14)
            addLabel(twin, "||", x + trans, 15)
            addLabel(twin, tbdate[trans], x + trans, 16)
            addLabel(twin, "|", x + trans, 17)
            addLabel(twin, tedate[trans], x + trans, 18)

        def update():
            tpricevar.set(pricevar.get() * qtyvar.get())
            duesvar.set(tpricevar.get() - payvar.get())
            if len(ttdues) == 0:
                tduesvar.set(0 + duesvar.get())
            else:
                tduesvar.set(ttdues[-1] + duesvar.get())
            addLabel(twin, tpricevar.get(), z, 8)
            addLabel(twin, tduesvar.get(), z, 14)

        def adnew():
            addLabel(twin, "|||", z, 1)
            i = addEntry(twin, itemvar, z, 2)
            addLabel(twin, "|", z, 3)
            p = addEntry(twin, pricevar, z, 4)
            addLabel(twin, "||", z, 5)
            q = addEntry(twin, qtyvar, z, 6)
            addLabel(twin, "|", z, 7)
            ub = addButton(z, 9, twin, 'LOAD', load_image, update)
            pa = addEntry(twin, payvar, z, 10)
            addLabel(twin, "|", z, 11)
            du = addEntry(twin, duesvar, z, 12)
            addLabel(twin, "|", z, 13)
            addLabel(twin, "||", z, 15)
            bdst = addButton(z, 17, twin, 'choosedate', date_image, bdateset)
            ed = addLabel(twin, edatevar.get(), z, 18)
            export = addButton(z + 1, 2, twin, 'Export', export_image, partial(export_csv, total))

            def selfdest(event):
                b.destroy()
                update()
                addt(i, p, q, ub, pa, du, bdst, ed, export)

            b = Button(master=twin, text="+", image=addnew_image)
            b.grid(row=z, column=0)
            b.bind("<1>", selfdest)

        adnew()

    welcomelabel = Label(tranwindow, text="Transactions for {}".format(lcname[cindex]))
    welcomelabel.pack()

    swin = ScrolledWindow(tranwindow, width=w - 80, height=h - 200)
    swin.pack(fill=X, expand=1)
    twin = swin.window

    refresh_t()

    tranwindow.mainloop()
