__author__ = 'iamhssingh'

from functools import partial
from tkinter import messagebox
from tkinter.tix import *

import compo.dbactions as actions
import compo.loggedin as log


# framebg = 'IndianRed1'
# labelbg = framebg
# labelfg = 'White'

# mainframebg = framebg
# buttonbg = 'Blue'
# reframebg = framebg


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


def addLabel(master, text, row, column, bg=None):
    if bg is not None:
        cname_label = Label(master=master, text=text, bg=bg, font=(12))
    elif bg is None:
        cname_label = Label(master=master, text=text, font=(12))
    cname_label.grid(row=row, column=column)
    return cname_label


def addEntry(master, textvar, row, column):
    new_entry = Entry(master=master, textvariable=textvar)
    new_entry.grid(row=row, column=column)
    return new_entry


def logmein():
    lstatus = actions.login(uname_var.get(), upwd_var.get())
    if len(lstatus) > 0:
        uid_var.set(lstatus[0])
        ufname_var.set(lstatus[1])
        ulname_var.set(lstatus[2])
        mainwindow.destroy()
        log.loggedin(uid_var.get(), ufname_var.get(), ulname_var.get())


def quit(window):
    c = messagebox.askyesno(title="Exit?", message="Are you sure you want to exit?")
    if c > 0:
        window.destroy()


def registerme(frame):
    rstatus.set(actions.register(uname_var.get(), ufname_var.get(), ulname_var.get(), upwd_var.get(), ucpwd_var.get()))
    if rstatus.get() == 1:
        frame.destroy()
        login()


def login():
    mainwframe.destroy()
    uname_var.set('')
    upwd_var.set('')
    mainwindow.geometry('480x180+600+250')
    mainwindow.title('Login to Business Management')

    mainframe = Frame(master=mainwindow, border=4, relief=RIDGE, padx=25, pady=25)
    mainframe.pack(expand=1, fill=BOTH)

    addLabel(mainframe, "User Name: ", 0, 0)
    addLabel(mainframe, "Password: ", 1, 0)
    addEntry(mainframe, uname_var, 0, 2)
    addEntry(mainframe, upwd_var, 1, 2)

    addLabel(mainframe, "                      ", 2, 0)
    addLabel(mainframe, "                      ", 2, 1)
    addLabel(mainframe, "                      ", 2, 2)

    addButton(3, 0, mainframe, "Login", login_image2, partial(logmein))
    addButton(3, 2, mainframe, "Cancel", cancel_image, partial(quit, mainwindow))
    addButton(4, 1, mainframe, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                          message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))
    addButton(4, 0, mainframe, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                          message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))
    addButton(4, 2, mainframe, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                          message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))


def register():
    mainwframe.destroy()
    mainwindow.geometry('450x255+600+250')
    mainwindow.title('Register a New User')

    register_frame = Frame(master=mainwindow, border=4, relief=RIDGE, padx=10, pady=25)
    register_frame.pack(expand=1, fill=BOTH)

    addLabel(register_frame, "                      ", 10, 0)
    addLabel(register_frame, "                      ", 10, 1)
    addLabel(register_frame, "                      ", 10, 2)
    addLabel(register_frame, "User Name: ", 1, 0)
    addLabel(register_frame, "First Name: ", 2, 0)
    addLabel(register_frame, "Last Name: ", 3, 0)
    addLabel(register_frame, "Password: ", 4, 0)
    addLabel(register_frame, "Confirm Password: ", 5, 0)
    addEntry(register_frame, uname_var, 1, 2)
    addEntry(register_frame, ufname_var, 2, 2)
    addEntry(register_frame, ulname_var, 3, 2)
    addEntry(register_frame, upwd_var, 4, 2)
    addEntry(register_frame, ucpwd_var, 5, 2)

    addButton(11, 2, register_frame, "Cancel", cancel_image, partial(quit, mainwindow))
    addButton(11, 0, register_frame, "Register", register_image, partial(registerme, register_frame))
    addButton(12, 0, register_frame, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                                message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))
    addButton(12, 1, register_frame, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                                message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))
    addButton(12, 2, register_frame, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                                message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))


def mainconfirm():
    if messagebox.askyesno("Quit", "Do you really wish to quit?"):
        mainwindow.destroy()


mainwindow = Tk()
mainwindow.geometry('375x150+600+250')
mainwindow.title("Accounts Management")
mainwindow.protocol("WM_DELETE_WINDOW", mainconfirm)
# mainwindow.iconbitmap("media/images/am.ico")

login_image = PhotoImage(file="media/images/login.gif")
login_image2 = PhotoImage(file="media/images/login2.gif")
register_image = PhotoImage(file="media/images/register.gif")
cancel_image = PhotoImage(file="media/images/cancel.gif")

mainwframe = Frame(master=mainwindow, border=4, relief=RIDGE, padx=4, pady=4)
mainwframe.pack(expand=1, fill=BOTH)

addLabel(mainwframe, "       ", 1, 1)
addLabel(mainwframe, "       ", 3, 1)
addButton(2, 1, mainwframe, "Log In", login_image, login)
addButton(2, 3, mainwframe, "Register Here", register_image, register)
addButton(4, 1, mainwframe, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                       message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))
addButton(4, 2, mainwframe, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                       message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))
addButton(4, 3, mainwframe, "About", None, lambda: messagebox.showinfo(title="About Creator",
                                                                       message="THIS APPLICATION IS A CREATION OF HIMANSHU SHANKAR"))

uname_var = StringVar()
upwd_var = StringVar()
uid_var = IntVar()
ufname_var = StringVar()
ulname_var = StringVar()
ucpwd_var = StringVar()

lstatus = []

rstatus = IntVar()

mainwindow.mainloop()
