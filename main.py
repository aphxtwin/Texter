from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog as fd
from tkinter import dialog
import tkinter
from PIL import Image, ImageTk
from tkinter import TclError
import os
import PIL

window = Tk()
window.title("Untitled - Texter")
window.iconbitmap(r"books.ico")
window.geometry("600x600")
window.resizable(True, True)

# ----------------------------------Textbox------------------------------------
txtr = Text(window, font="Arial", undo=True)
scroll_bar = Scrollbar(window)

txtr.focus_set()
toolbar = Label(window, relief="raise")
scroll_bar.pack(side=RIGHT, fill=Y)
toolbar.pack(side="top", fill=BOTH, expand=False)
txtr.pack(fill=BOTH, expand=TRUE)
# -----------------------------------------------------------------------------
global open_id
open_id = False

menubar = Menu(window)
# -----------------------------------TOOLBAR------------------------------------#


# -------------------------FILE FUNCTIONS--------------------------------#
def delete_alltxtr():
    txtr.delete("1.0", "end-1c")
    anykeypressed(event=True)


def new():
    global open_id
    open_id = False
    delete_alltxtr()
    window.title("Untitled - Texter")
    anykeypressed(event=True)


def new_if():
    if open_id is not False:
        with open(open_id) as f:
            comparison = f.read()
            if comparison == txtr.get("1.0", "end-1c"):
                new()
            else:
                ans = messagebox.askyesnocancel(
                    title="Texter", message="Do you want to save changes?"
                )
                if ans == True:
                    save()
                    new()
                if ans == False:
                    new()
    elif txtr.compare("1.0", "!=", "end-1c"):
        ans = messagebox.askyesnocancel(
            title="Texter", message="Do you want to save changes?"
        )
        if ans == True:
            save_as()
            delete_alltxtr()
        if ans == False:
            delete_alltxtr()


def quit_secure():
    if open_id == False:
        if txtr.compare("1.0", "!=", "end-1c"):
            ans = messagebox.askyesnocancel(
                title="Texter", message="Do you want to save changes?"
            )
            if ans == True:
                save_as()
                window.quit()
            if ans == False:
                window.quit()
        else:
            window.quit()
    elif open_id is not False:
        ans = messagebox.askyesnocancel(
            title="Texter", message="Do you want to save changes?"
        )
        if ans == False:
            quit()
        if ans == True:
            save()
            window.quit()


def openit():
    global open_id
    filename = fd.askopenfile(
        initialdir=os.getcwd(),
        title="Open",
        filetypes=[("text files", "*.txt"), ("all files", "*.*")],
        mode="r",
    )
    if filename is not None:
        open_id = filename.name
        delete_alltxtr()
        content = filename.read()
        txtr.insert("1.0", chars=content)
        anykeypressed(event=True)
        rename()
        filename.close()


def save_as():
    global open_id
    filename = fd.asksaveasfile(
        mode="w",
        title="Save as",
        initialdir=os.getcwd(),
        filetypes=[("text files", "*.txt"), ("all files", "*.*")],
        defaultextension="*.txt",
    )
    if filename is not None:
        writes = txtr.get("1.0", "end-1c")
        filename.write(writes)
        global open_id
        open_id = filename.name

        filename.close()
        rename()


def save():
    global open_id
    if open_id == False:
        filename = fd.asksaveasfile()
        open_id = filename.name
    else:
        content = txtr.get("1.0", "end-1c")
        with open(open_id, mode="w") as f:
            f.write(content)


def anykeypressed(event):
    tr = ["0","1","2","3","4","6"]
    if len(txtr.get("1.0", "end-1c")) == 0:
        for i in tr:
            edit.entryconfig(i, state="disabled")
    if len(txtr.get("1.0", "end-1c")) > 0:
        for i in tr:
            edit.entryconfig(i, state="normal")


def rename():
    name = os.path.basename(open_id)
    window.title(f"{name} - Texter")


# ---------------------------EDIT FUNCTIONS----------------------------#


# EDIT IMAGES#
with Image.open(r"images\redo.png") as f:
    img_redo = f.resize(((20, 20)), Image.Resampling.LANCZOS)
    redoico = ImageTk.PhotoImage(img_redo)
with Image.open(r"images\undo.png") as f:
    img_undo = f.resize((20, 20), Image.Resampling.LANCZOS)
    undoico = ImageTk.PhotoImage(img_undo)
with Image.open(r"images\cut.png") as f:
    img_cut = f.resize((20, 20), Image.Resampling.LANCZOS)
    cutico = ImageTk.PhotoImage(img_cut)
with Image.open(r"images\copy.png") as f:
    img_copy = f.resize((20, 20), Image.Resampling.LANCZOS)
    copico = ImageTk.PhotoImage(img_copy)
with Image.open(r"images\paste.png") as f:
    img_paste = f.resize((20, 20), Image.Resampling.LANCZOS)
    pastico = ImageTk.PhotoImage(img_paste)
with Image.open(r"images\find.png") as f:
    img_find = f.resize((20, 20), Image.Resampling.LANCZOS)
    findico = ImageTk.PhotoImage(img_find)
with Image.open(r"images\all.png") as f:
    img_selectall = f.resize((20, 20), Image.Resampling.LANCZOS)
    selectallico = ImageTk.PhotoImage(img_selectall)
with Image.open(r"images\eraser.png") as f:
    img_eraser = f.resize((20, 20), Image.Resampling.LANCZOS)
    eraserico = ImageTk.PhotoImage(img_eraser)

##Copy function
def copy():
    try:
        window.clipboard_clear()
        cliptext = window.clipboard_append(txtr.selection_get())
        window.update()
    except tkinter.TclError:
        pass


##Paste function
def paste():
    try:
        content = window.clipboard_get()
        txtr.insert(INSERT, chars=content)
    except tkinter.TclError:
        pass


##Cut function
def cut():
    try:
        copy()
        indx1 = txtr.index("sel.first")
        indx2 = txtr.index("sel.last")
        txtr.delete(indx1, indx2)
    except tkinter.TclError:
        pass


##Find function
def find_label():
    """
    Creation of the TopLevel
    """
    findi = Toplevel(window)
    findi.title("Find")
    findi.resizable(0, 0)
    findi.iconbitmap(r"books.ico")
    findi.geometry("340x100+300+300")
    # entry class
    entri = Entry(findi, width=25, font="arial", exportselection=0, justify="center")
    entri.place(x=35, y=15, width=282)
    entri.focus_set()
    # find button
    def find():
        txtr.tag_remove("find", "1.0", END)
        seek_word = entri.get().split()
        txtr.tag_config("find", foreground="white", background="blue")
        for i in seek_word:
            idx = "1.0"
            while True:
                idx = txtr.search(i, idx, nocase=1, stopindex="end-1c")
                if idx:
                    lastidx = "%s+%dc" % (idx, len(i))
                    txtr.tag_add("find", idx, lastidx)
                    idx = lastidx
                else:
                    break

    findibuttonfind = Button(findi, text="Find", width=10, command=find)
    findibuttonfind.place(relx=0.1, rely=0.5)

    def destroyer():
        txtr.tag_remove("find", "1.0", "end")
        findi.destroy()

    findibuttoncancel = Button(findi, text="Cancel", width=10, command=destroyer)
    findibuttoncancel.place(relx=0.7, rely=0.5)
    # delete button
    def reset():
        txtr.tag_remove("find", "1.0", END)
        entri.delete(0, END)
        entri.insert(0, "")

    findibuttondelete = Button(findi, text="Reset", width=10, command=reset)
    findibuttondelete.place(relx=0.4, rely=0.5)
    findi.protocol("WM_DELETE_WINDOW", destroyer)


##Select all function
def select_all():
    try:
        txtr.tag_add("sel", "1.0", "end")
    except tkinter.TclError:
        pass


def show_hide_t():
    global hidden
    if hidden == False:
        options.entryconfig(1, label="Show toolbar")
        toolbar.pack_forget()
        hidden = True
    else:
        options.entryconfig(1, label="Hide toolbar")
        txtr.pack_forget()
        toolbar.pack(side="top", fill=X, expand=False)
        txtr.pack(fill=BOTH, expand=True)
        hidden = False


hidden = False

# ---------------------------------------THE MENU ----------------------------------------------------#E
##FILE SUBMENU
file = Menu(menubar, tearoff=0)
file.add_command(label="New", command=new_if)
file.add_command(label="Open", command=openit)
file.add_command(label="Save", command=save)
file.add_command(label="Save as", command=save_as)
file.add_separator()

file.add_command(label="Exit", command=quit_secure)
menubar.add_cascade(label="File", menu=file)

##EDIT SUBMENU

edit = Menu(menubar, tearoff=0)
edit.add_command(label="Undo", image=undoico, state=DISABLED, compound="left",command=txtr.edit_undo)
edit.add_command(label="Redo", image=redoico,state=DISABLED, compound="left",command=txtr.edit_redo)
edit.add_command(label="Cut", image=cutico,state=DISABLED, compound="left", command=cut)
edit.add_command(label="Copy", image=copico, state=DISABLED, compound="left", command=copy)
edit.add_command(label="Paste", image=pastico,state=DISABLED, compound="left", command=paste)

edit.add_separator()

edit.add_command(
    label="Find", image=findico, state="disabled", compound="left", command=find_label
)
edit.add_command(
    label="Select all", image=selectallico, compound="left", command=select_all
)
edit.add_command(
    label="Clear all", compound="left", command=delete_alltxtr, image=eraserico
)

menubar.add_cascade(label="Edit", menu=edit)
##options submenu
options = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=options)

options.add_command(label="Hide toolbar", command=show_hide_t)
##HELP SUBMENU
help = Menu(menubar, tearoff=0)
help.add_command(label="About texter")
menubar.add_cascade(label="Help", menu=help)

window.config(menu=menubar)
# ------------------------PROTOCOL MODIFICATIONS---------------------#
window.protocol("WM_DELETE_WINDOW", quit_secure)

# -------------------------binds---------------------------------------#
txtr.bind("<KeyRelease>", anykeypressed)
window.mainloop()
