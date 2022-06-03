#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created in Jul 2021

@author: Ernest (Khashayar) Namdar

##############################################################################
# Based on Hajime Nakagami's viewer
#
# Pillow is required( https://pypi.python.org/pypi/Pillow/ ).
##############################################################################
"""
import PIL.Image
try:
    # from Tkinter import *
    from Tkinter import Tk
    from Tkinter import Frame
    from Tkinter import Button, Label, StringVar
    from Tkinter import LEFT, TOP, BOTTOM, BOTH
    import tkFileDialog as filedialog
except ImportError:
    # from tkinter import *
    from tkinter import Tk
    from tkinter import Frame
    from tkinter import Button, Label, StringVar, Entry
    from tkinter import LEFT, TOP, BOTTOM, BOTH
    from tkinter import filedialog
import PIL.ImageTk
import os
import numpy as np

def nextFile(filename, directory, backward=False):
    fileList = os.listdir(directory)
    if backward:
        nextIndex = fileList.index(filename) - 1
    else:
        nextIndex = fileList.index(filename) + 1
    if nextIndex == 0 or nextIndex == len(fileList):
        return None
    return os.path.join(directory, fileList[nextIndex])


class IMICS_viewer(Frame):
    def chg_image(self):
        if self.im.mode == "1":  # bitmap image
            self.img = PIL.ImageTk.BitmapImage(self.im, foreground="white")
        else:              # photo image
            self.img = PIL.ImageTk.PhotoImage(self.im)
        self.la.config(image=self.img, bg="#000000",
                       width=self.img.width(), height=self.img.height())

    def open(self, filename=None):
        if filename is None:
            filename = filedialog.askopenfilename()
        self.imdirname, self.imfilename = os.path.split(filename)
        if filename != "":
            if filename.lower().endswith(".npy"):
                self.nparray = np.load(os.path.join(self.imdirname, self.imfilename))
                self.current_ind_int = 0
                self.im = PIL.Image.fromarray(self.nparray[self.current_ind_int])
                print(self.im.mode)
                self.current_ind.set(str(self.current_ind_int))
                self.img = PIL.ImageTk.PhotoImage(self.im)
                self.la.config(image=self.img, bg="#000000",
                               width=self.img.width(),
                               height=self.img.height())
                self.img_row.set(str(self.img.height()))
                self.img_col.set(str(self.img.width()))
                self.array_len.set(str(self.nparray.shape[0]))
            else:
                self.im = PIL.Image.open(os.path.join(self.dirpath, "FiletypeErr.png"))
                self.img = PIL.ImageTk.PhotoImage(self.im)
                self.la.config(image=self.img, bg="#000000",
                                   width=self.img.width(),
                                   height=self.img.height())
                self.img_row.set("___")
                self.img_col.set("___")
        self.chg_image()

    def seek_prev(self):
        if self.current_ind_int <= 0:
            self.im = PIL.Image.open(os.path.join(self.dirpath,"First.png"))
            self.img = PIL.ImageTk.PhotoImage(self.im)
            self.la.config(image=self.img, bg="#000000",
                           width=self.img.width(), height=self.img.height())
            print("Came to the first file")
            self.current_ind_int = -1
        else:
            self.current_ind_int -= 1
            self.im = PIL.Image.fromarray(self.nparray[self.current_ind_int])
            self.current_ind.set(str(self.current_ind_int))
            self.img = PIL.ImageTk.PhotoImage(self.im)
            self.la.config(image=self.img, bg="#000000",
                           width=self.img.width(),
                           height=self.img.height())
            self.img_row.set(str(self.img.height()))
            self.img_col.set(str(self.img.width()))

    def seek_next(self):
        if self.current_ind_int >= self.nparray.shape[0]-1:
            self.im = PIL.Image.open(os.path.join(self.dirpath,"Last.png"))
            self.img = PIL.ImageTk.PhotoImage(self.im)
            self.la.config(image=self.img, bg="#000000",
                           width=self.img.width(), height=self.img.height())
            print("Came to the last file")
            self.current_ind_int = self.nparray.shape[0]
        else:
            self.current_ind_int += 1
            self.im = PIL.Image.fromarray(self.nparray[self.current_ind_int])
            self.current_ind.set(str(self.current_ind_int))
            self.img = PIL.ImageTk.PhotoImage(self.im)
            self.la.config(image=self.img, bg="#000000",
                           width=self.img.width(),
                           height=self.img.height())
            self.img_row.set(str(self.img.height()))
            self.img_col.set(str(self.img.width()))

    def go(self):
        ind = self.current_ind.get()
        try:
            ind = int(ind)
        except:
            ind = None
        if ind is None:
            self.current_ind.set("Invalid Index")
        if ind >= self.nparray.shape[0] or ind < 0:
            self.current_ind.set("Invalid Index")
        else:
            self.current_ind_int = ind
            self.im = PIL.Image.fromarray(self.nparray[self.current_ind_int])
            self.current_ind.set(str(self.current_ind_int))
            self.img = PIL.ImageTk.PhotoImage(self.im)
            self.la.config(image=self.img, bg="#000000",
                           width=self.img.width(),
                           height=self.img.height())
            self.img_row.set(str(self.img.height()))
            self.img_col.set(str(self.img.width()))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('IMICS Numpy Image Viewer')
        self.master.minsize(400, 470)
        self.master.resizable(True, True)

        fram = Frame(self)
        Button(fram, text="Open File", command=self.open).pack(side=LEFT)
        Button(fram, text="Prev", command=self.seek_prev).pack(side=LEFT)
        Label(fram, text="Current Index:").pack(side=LEFT)
        self.current_ind = StringVar()
        self.current_ind.set("--")
        Entry(fram, textvariable=self.current_ind, bd =1).pack(side=LEFT)
        Button(fram, text="Go", command=self.go).pack(side=LEFT)
        Button(fram, text="Next", command=self.seek_next).pack(side=LEFT)
        fram.pack(side=TOP, fill=BOTH)

        self.la = Label(self)
        self.la.pack()
        self.dirpath = os.path.dirname(os.path.realpath(__file__))
        self.im = PIL.Image.open(os.path.join(self.dirpath,"Welcome.png"))
        self.img = PIL.ImageTk.PhotoImage(self.im)
        self.la.config(image=self.img, bg="#000000",
                       width=self.img.width(), height=self.img.height())

        self.img_row = StringVar()
        self.img_col = StringVar()
        self.array_len = StringVar()
        self.img_row.set('--')
        self.img_col.set('--')
        self.array_len.set('--')
        fram2 = Frame(self)
        Label(fram2, text="Image Rows:  ").pack(side=LEFT)
        Label(fram2, textvariable=self.img_row).pack(side=LEFT)
        Label(fram2, text="Image Columns:  ").pack(side=LEFT)
        Label(fram2, textvariable=self.img_col).pack(side=LEFT)
        Label(fram2, text="Array Length:  ").pack(side=LEFT)
        Label(fram2, textvariable=self.array_len).pack(side=LEFT)
        fram2.pack(side=BOTTOM, fill=BOTH)

        self.pack()


def main():
    root = Tk()
    IMICS_viewer(root)  # Defining the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
