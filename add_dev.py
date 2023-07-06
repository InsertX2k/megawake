"""
The Add devices module for megawake

Importing this module while developing megawake allows megawake to:

* Launch the window that asks user for information about the device they want to save
* Access Defined Exception classes in this module for later use in other programs or even in megawake itself
* Append new items at the end of the saved devices list (CSV File)

License: 

    A module for adding new devices to the CSV file megawake uses to store the list of saved devices.
    
    Copyright (C) 2023 Insertx2k Dev (Mr.X) or Ziad Ahmed (Mr.X)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
# imports
from tkinter import *
from tkinter import ttk, messagebox

# -------------------------------------------------------
import os
import sys

# initializing a variable containing the path where application files are stored.
application_path = ''

# attempting to get where the program files are stored
if getattr(sys, 'frozen', False): 
    # if program was frozen (compiled) using pyinstaller, the pyinstaller bootloader creates a sys attribute
    # frozen=True to indicate that the script file was compiled using pyinstaller, then it creates a
    # constant in sys that points to the directory where program executable is (where program files are extracted in).
    application_path = sys._MEIPASS
else: 
    # if program is not frozen (compiled) using pyinstaller and is running normally like a Python 3.x.x file.
    application_path = os.path.dirname(os.path.abspath(__file__))

# changing the current working directory to the path where one-file mode source files are extracted in.
os.chdir(application_path)
# -------------------------------------------------------


class AddNewSavedDeviceWindow(Toplevel):
    def __init__(self, runAfterSaveFunc, savedDevicesListFileName=f"{application_path}\\saved_devs.csv") -> None:
        """
        Window for adding a new device to save.

        Required arguments:
        
        `runAfterSaveFunc` - Specifies the name of a function to run after the saving process is done, for example `Update` function.

        Optional arguments:

        `savedDevicesListFileName` - the full File Name for the CSV File to save the device to
        """
        super().__init__()
        self.title("Add New Device")
        self.geometry('500x280')
        self.resizable(True, True)
        self.savedDevicesListFileName = savedDevicesListFileName
        self.runAfterSaveFunc = runAfterSaveFunc

        # adding widgets
        self.lbl0 = Label(self, text="Save a new device", font=("Arial Bold", 15), foreground='black')
        self.lbl0.pack(anchor=W)
        self.lbl_warn = Label(self, text="WARNING: Inserting commas in any of these fields (,)\n can cause problems, so please avoid using them whenever possible", font=("Arial", 11), foreground='red', anchor=W)
        self.lbl_warn.pack(anchor=W)
        try:
            self.iconbitmap(f"{application_path}\\icon1.ico")
        except Exception as errorApplyingIconBitmap:
            messagebox.showerror("Runtime Error", f"Unable to apply iconbitmap to the current window because of an error\nPlease restart megawake\n\nError details for technical support:\n{errorApplyingIconBitmap}")
            pass

        def closeBtnAction():
            """
            A function for the close button.
            """
            self.destroy()
            return None
        
        def addSavedDeviceAction():
            """
            A function used to save a new device to the CSV List.
            """
            print(f"[DEBUG]: Will save device name: '{self.devname_insert_entry.get()}' from manufacturer: '{self.devman_insert_entry.get()}' and model: '{self.devmodel_insert_entry.get()}', with mac address of: {self.devmacaddr_insert_entry.get()}")
            try:
                save_file_handler = open(self.savedDevicesListFileName, mode='a', encoding='utf-8')
            except Exception as errorOpeningFileToSaveIn:
                messagebox.showerror("Runtime Error", f"Couldn't open the file {self.savedDevicesListFileName} to save this device in\nPlease make sure it exists in the current program directory and try again\nPress OK to close this window\n\nError details for technical support:\n{errorOpeningFileToSaveIn}")
                self.destroy()
                return False
            
            try:
                device_manufacturer = str(self.devman_insert_entry.get())
                device_name = str(self.devname_insert_entry.get())
                device_model = str(self.devmodel_insert_entry.get())
                device_macaddr = str(self.devmacaddr_insert_entry.get())
                if device_macaddr == '':
                    messagebox.showerror("Error", "You can't save a device without a Mac Address!")
                    return False
            except:
                self.destroy()
                return False
            try:
                # now let's write the list to the file
                save_file_handler.write(f"{device_name},{device_manufacturer},{device_model},{device_macaddr}\n")
                save_file_handler.close()
            except Exception as errorWritingToCSVFile:
                messagebox.showerror("Save Error", f"An error has occured while trying to add your device to saved devices list\nPlease restart megawake and try again later\n\nError details for technical support:\n{errorWritingToCSVFile}")
                self.destroy()
                return False
            
            messagebox.showinfo("Add Device", f"Successfully saved device {device_name}!")
            self.destroy()
            self.runAfterSaveFunc()
            return None
        
        self.lbl1 = Label(self, text="Device Name:", font=("Arial", 11), foreground='black')
        self.lbl1.pack(anchor=W)
        self.devname_insert_entry = ttk.Entry(self)
        self.devname_insert_entry.pack(anchor=W, fill=X)
        self.lbl2 = Label(self, text="Manufacturer:", font=("Arial", 11), foreground='black')
        self.lbl2.pack(anchor=W)
        self.devman_insert_entry = ttk.Entry(self)
        self.devman_insert_entry.pack(anchor=W, fill=X)
        self.lbl3 = Label(self, text="Device Model:", font=("Arial", 11), foreground='black')
        self.lbl3.pack(anchor=W)
        self.devmodel_insert_entry = ttk.Entry(self)
        self.devmodel_insert_entry.pack(anchor=W, fill=X)
        self.lbl4 = Label(self, text="Mac Address:", font=("Arial", 11), foreground='black')
        self.lbl4.pack(anchor=W)
        self.devmacaddr_insert_entry = ttk.Entry(self)
        self.devmacaddr_insert_entry.pack(anchor=W, fill=X)
        
        # defining widgets inside of that action frame
        self.add_btn = ttk.Button(self, text="Save", command=addSavedDeviceAction)
        self.add_btn.pack(side=RIGHT, anchor=E, ipadx=15)
        self.close_btn = ttk.Button(self, text="Close", command=closeBtnAction)
        self.close_btn.pack(side=RIGHT, anchor=E, ipadx=15)



def empty():
    pass


if __name__ == '__main__':
    # test = AddNewSavedDeviceWindow(empty)
    # test.mainloop()
    pass