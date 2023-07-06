"""
The error window module for megawake

Importing this module while developing megawake allows you to:

* Access various Exception classes this module offers.
* Display Errors in the form of a window.
"""
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


# imports
from tkinter import *
from tkinter import ttk, messagebox, scrolledtext

class ErrorWindow(Tk):
    def __init__(self, errorText='') -> None:
        super().__init__()
        self.title("Error while starting megawake")
        self.geometry('450x225')
        self.resizable(False, False)
        self.wm_resizable(False, False)
        self.errorText = errorText
        try:
            self.iconbitmap(f"{application_path}\\icon1.ico")
        except Exception as errorApplyingIconBitmap:
            messagebox.showerror("Runtime Error", f"An error has occured while trying to apply the iconbitmap for this window\nPlease restart megawake\n\nError details for technical support:\n{errorApplyingIconBitmap}")
        
        def closeMW():
            """
            The function for closing megawake.
            """
            self.destroy()
            raise SystemExit(300) # system.exit 300 is for unhandled error.
            return None
        
        def insertErrorInformation(errorText=''):
            """
            Inserts error information into the scrolledtext widget in order to show them to the user.
            """
            self.errorinfo.configure(state='normal')
            self.errorinfo.delete(1.0, END)
            self.errorinfo.insert(END, f"""An error has occured causing megawake to terminate it's process unexpectedly or even fail to start.
You (as a user) can do all (or any) of the following in case of an error:
* Restarting megawake
* Creating an issue on megawake's official github repository (https://github.com/InsertX2k/megawake)
* Reinstalling megawake
                                  
More error details in case of the need to technical assistance: 

{errorText}
""")
            self.errorinfo.configure(state='disabled')
            return None
        
        self.pack_propagate(True)
        self.errorinfo = scrolledtext.ScrolledText(self, state='disabled', selectbackground='cyan', highlightcolor='cyan', height=12)
        self.errorinfo.pack(fill=BOTH, expand=False)

        self.close_btn = ttk.Button(self, text="Close megawake", command=closeMW)
        self.close_btn.pack(fill=BOTH, expand=False)

        # self.protocol("WM_DELETE_WINDOW", closeMW)
        insertErrorInformation(self.errorText)
        



if __name__ == '__main__':
    # test = ErrorWindow()
    # test.mainloop()
    pass
