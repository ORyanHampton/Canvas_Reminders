import os
import plistlib
import pathlib
import logging
import sys
import subprocess
import Canvas_TODO_grab
# import PIL

import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
# from PIL import Image, ImageTk

class canvas_reminders_driver(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        root = ttk.Frame(self)

        root.pack(side='top', fill='both', expand=True)

        self.frames = {}

        F = Collection_Page
            
        frame = F(root, self)

        self.frames[F] = frame

        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Collection_Page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Collection_Page(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        def create_file():
            url = nameBox.get() or None
            reminders = listBox.get() or None
            authKey = keyBox.get() or None

            currentDir = pathlib.Path(__file__).parent.absolute().parent.parent
            filePath = currentDir/"api_keys"

            f = open(filePath, 'w+')

            f.write(f"API_URL={url}")
            f.write("\n")
            f.write(f"API_KEY={authKey}")
            f.write("\n")
            f.write(f"LIST_NAME={reminders}")
            f.close()

            Canvas_TODO_grab.reminder_logic()

            finishedWindow()

        """
        ********************************************* Title ***********************************************
        """
        frame0 = ttk.Frame(self)
        frame0.pack(fill='x')

        headerLabel = ttk.Label(self, text='Canvas Reminders Setup', font=('Courier', 18))
        headerLabel.pack(side='top', pady='10')

        
        """
        ******************************* Institution URL ************************************************
        """
        frame1 = ttk.Frame(self)
        frame1.pack(fill='x')

        nameLabel = ttk.Label(frame1, text='Institution URL: ')
        nameLabel.pack(side='left', anchor='n', padx='10')

        nameBox = ttk.Entry(frame1)
        nameBox.pack(side='left', anchor='n', expand=True, fill='both', padx='10')

        """
        ******************************* Reminders List ************************************************
        """
        frame2 = ttk.Frame(self)
        frame2.pack(fill='x')

        listLabel = ttk.Label(frame2, text='Reminders List: ')
        listLabel.pack(side='left', anchor='n', padx='10')

        listBox = ttk.Entry(frame2)
        listBox.pack(side='left', anchor='n', expand=True, fill='both', padx='10')

        """
        ******************************* Canvas Login Key ************************************************
        """
        frame3 = ttk.Frame(self)
        frame3.pack(fill='x')

        keyLabel = ttk.Label(frame3, text='Canvas Auth Key:')
        keyLabel.pack(side='left', anchor='n', padx='5.4')

        keyBox = ttk.Entry(frame3)
        keyBox.pack(side='left', anchor='n', expand=True, fill='both', padx='11')

        """
        ******************************* Buttons ************************************************
        """
        frame8 = ttk.Frame(self)
        frame8.pack(fill='x')

        submitButton = ttk.Button(frame8, text='OK', command=lambda: create_file())
        submitButton.pack(side='right', pady='15', padx='20')

        backButton = ttk.Button(frame8, text='Quit', command=lambda: sys.exit(0))
        backButton.pack(side='left', pady='15', padx='20')

def finishedWindow():
    finishedWindow = tk.Tk()
    finishedWindow.title('Process Completed')

    finishedWindow.configure(bg='#eaebeb')

    finishedLabel = ttk.Label(finishedWindow, text='Canvas Reminders Setup Complete.')
    finishedLabel.pack(side='top')

    finishedButton = ttk.Button(finishedWindow, text='Okay', command=lambda: sys.exit())
    finishedButton.pack(side='bottom')

    center(finishedWindow)

def errorWindow(err):
    errorWindow = tk.Tk()
    errorWindow.title('Setup Error')

    errorWindow.configure(bg='#eaebeb')

    errorLabel = ttk.Label(errorWindow, text=f'An Error Occured: {err}')
    errorLabel.pack(side='top')

    errorButton = ttk.Button(errorWindow, text='Okay', command=lambda: sys.exit())
    errorButton.pack(side='bottom')

    center(errorWindow)


def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def main():
    app = canvas_reminders_driver()
    app.title('Canvas Reminders Setup')
    center(app)
    app.mainloop()

if __name__ == "__main__":
    main()