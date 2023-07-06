"""
MegaWake - A wake on lan program for x86_64-based Computers (PCs running Windows and Linux Operating Systems)

Licensed under the GNU General Public License v2.0 or later @ Free Software Foundation.

Copyright (C) 2022 - 2023 - Ziad Ahmed aka. Insertx2k Dev (Mr.X)
"""

# -------------------------
# fixes for python and pyinstaller and necessary for bundling 3rd party non-binary files within the program.
# imports necessary to get the path where the files are extracted in
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

# -------------------------


# -------------------------
# fixes for pyinstaller when showing console window when gui is launched.

if sys.platform.lower().startswith('win'):
    import ctypes

    def hideConsole():
        """
        Hides the console window in GUI mode. Necessary for frozen application, because
        this application support both, command line processing AND GUI mode and theirfor
        cannot be run via pythonw.exe.
        """

        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            # if you wanted to close the handles...
            #ctypes.windll.kernel32.CloseHandle(whnd)

    def showConsole():
        """Unhides console window"""
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 1)

# -------------------------


from tkinter import *
from tkinter import ttk, messagebox
# from customtkinter import *
from wakeonlan import send_magic_packet
from psutil import net_if_addrs
from sys import argv
from colorama import Fore, Style, init
import csv
import csv_writer
import add_dev
import error_window


# initializing colorama.
init(autoreset=True)

# network interfaces lists.
network_interfaces = []
network_interfaces_local_ips = []

# string for storing the full path of the saved devices CSV File.
saved_devs_list_full_path = f"{application_path}\\saved_devs.csv"


class MainWindow(Tk):
    def __init__(self) -> None:
        global network_interfaces, network_interfaces_local_ips, saved_devs_list_full_path
        super().__init__()
        self.title("megawake")
        self.geometry('750x500')
        # self.minsize(750,600)
        self.resizable(True, True)
        self.configure(background='#333')
        # customtkinter related configuration
        # deactivate_automatic_dpi_awareness()
        # try:
        #     set_appearance_mode("dark")
        #     set_default_color_theme("blue")
        # except Exception as errorApplyingCTKTheme:
        #     messagebox.showerror("Error in Runtime", f"An error has occured while applying theme blue\nError details are:\n{errorApplyingCTKTheme}\n\nPress any key to close this window therefore closing the program.")
        #     self.destroy()
        #     raise SystemExit(500) # sys.exit 500 is for unhandled theming exception

        try:
            self.iconbitmap("icon1.ico")
        except Exception as icon_loading_error:
            messagebox.showerror("Window traceback", f"Couldn't load the iconbitmap for this window due to the exception\n{icon_loading_error}")
            pass
        
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=False)

        self.lbl0 = Label(self.main_frame, text="Wake on Lan options:", font=("Arial", 11), foreground='black').pack(anchor=W)

        def get_interface_information():
            print("[INFO] get interface function called.")
            print(self.network_interfaces_combo.current())
            print(f"[INFO] Current selected network interface Local IP Address is: {network_interfaces_local_ips[self.network_interfaces_combo.current()]}")
            return str(network_interfaces_local_ips[self.network_interfaces_combo.current()])
        
        def wake_on_lan():
            print("[INFO] Sent a wake on lan event.")
            mac_address = self.macaddress_entry.get()
            mac_address = mac_address.upper()
            if mac_address == '':
                messagebox.showerror("Wake on Lan", "Mac Address can not be empty.")
                return False
            
            if int(self.port_combobox.current()) == 0:
                print("[INFO] Chosen WoL port is 7")
                wol_port = 7
            elif int(self.port_combobox.current()) == 1:
                print("[INFO] Chosen WoL port is 9")
                wol_port = 9
            else:
                messagebox.showerror("Wake on Lan", "Invalid choice on WoL port combobox")
                return False
            
            try:
                interface_local_ip = str(get_interface_information())
                print(interface_local_ip)
            except Exception as cant_get_interface_local_ip:
                messagebox.showerror("Network Interface retrievation error", f"Can't get network interface's local IP address\nError details are:\n{cant_get_interface_local_ip}\n\nWe recommend that you restart the program and try again.")
                return False
            
            try:
                send_magic_packet(mac_address, interface=interface_local_ip, port=wol_port)
                messagebox.showinfo("Wake on Lan", f"Sent Wake on Lan (WoL) packet to device {mac_address} on port {wol_port}")
            except Exception as wol_packet_send_error:
                messagebox.showerror("Wake on Lan", f"Can't send a magic packet request to {mac_address}, on port: {wol_port}, on network interface: {interface_local_ip}\nDue to the following error:\n{wol_packet_send_error}\n\nYou can restart your computer and try again.")
                return False
            
            
            return True

        def read_from_csv_save(fileName=saved_devs_list_full_path):
            """
            Attempts to read from the CSV file that stores all the saved devices then inserts it's content on the TreeView widget of saved devices.

            Returns False when an error happens, and returns True when it creates a new file, if all fails it returns False
            """
            # clearing tree view area.
            try:
                for item in self.saveddevs_treeview.get_children():
                    self.saveddevs_treeview.delete(item)
            except:
                pass
            # checking if file exists.
            try:
                with open(fileName, mode='r', encoding='utf-8') as read_csv_file:
                    reader = csv.reader(read_csv_file)
                    for dev in reader:
                        self.saveddevs_treeview.insert('', END, values=dev)
                read_csv_file.close() # IMPORTANT!!!
            except Exception as errorReadingCSVFile:
                messagebox.showerror("Error", f"Can't read from the file that stores the list of saved devices.\nmegawake will attempt to create a new one for you.\n\nError details for technical support:\n{errorReadingCSVFile}")
                try:
                    with open(fileName, mode='w', encoding='utf-8') as new_csv_file:
                        new_csv_file.write("Example Device,Ziad (Mr.X) Software,Example Model,XX-XX-XX-XX-XX-XX")
                    new_csv_file.close()
                    with open(fileName, mode='r', encoding='utf-8') as read_new_csv_file:
                        reader = csv.reader(read_new_csv_file)
                        for dev in reader:
                            self.saveddevs_treeview.insert('', END, values=dev)
                    read_new_csv_file.close() # IMPORTANT!!!
                    return True
                except Exception as errorCreatingNewCSVFile:
                    messagebox.showerror("Runtime Error", f"megawake failed to create the file that will store saved devices\nPlease close this program and try again\n\nError details for technical support:\n{errorCreatingNewCSVFile}")
                    self.destroy()
                    raise SystemExit(500) # sys.exit 500 is for unhandled error that caused megawake to fail creating new csv file.
                    return False
            
            
            return None


        def delete_selected_saved_device(fileName=saved_devs_list_full_path):
            """
            Deletes the selected device(s) from the CSV files that stores saved devices then refreshes the TreeView to ensure it lists the current values only

            Returns False when an error occurs, otherwise returns None.

            **THIS FUNCTION IS INCOMPLETE**
            """
            # NEEDS A REWRITE
            devs = []
            try:
                for device in self.saveddevs_treeview.get_children():
                    devs.append(self.saveddevs_treeview.item(device)['values'])
            except:
                pass
            print(f"[DEBUG]: Value for devs is: {devs}")
            try:
                for selected_dev in self.saveddevs_treeview.selection():
                    print(selected_dev)
                    item = self.saveddevs_treeview.item(selected_dev)
                    dev_name = str(item['values'][0])
                    print(f"[DEBUG]: Deleting: {dev_name}")
                    for dev in devs:
                        if dev_name in dev:
                            devs.remove(dev)
            except:
                messagebox.showerror("Delete?", "Select something from the list to delete")
                return False
            
            print(f"[DEBUG]: Value for devs after deleting item: {devs}")
            # with open(fileName, mode='w', encoding='utf-8') as write_to_csv_file:
            #     writer = csv.writer(write_to_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     print(devs)
            #     # writer.writerows(devs)
            #     for dev in devs:
            #         if dev == '':
            #             pass
            #         else:
            #             writer.writerow(dev)
            # write_to_csv_file.close() # IMPORTANT!!!
            try:
                csv_writer.write_list_to_csv_file(fileName, devs)
            except Exception as errorInCSVWriterModule:
                messagebox.showerror("Runtime Error", f"An error has occured during the execution of the CSV Writer module\nPlease restart this program\n\nError details for technical support:\n{errorInCSVWriterModule}")
                return False
            
            # refresh
            read_from_csv_save()
            
            return None

        def startSaveNewDeviceWindow(fileName=saved_devs_list_full_path):
            """
            A function for the button to save a new device to the saved devices CSV File.
            """
            add_dev.AddNewSavedDeviceWindow(read_from_csv_save, savedDevicesListFileName=fileName)
            return None
    
        
        self.lbl2 = Label(self.main_frame, text="Choose Network Interface:", font=("Arial", 11), foreground='black').pack(anchor=W)
        self.network_interfaces_combo = ttk.Combobox(self.main_frame)
        self.network_interfaces_combo['values'] = network_interfaces
        self.network_interfaces_combo.current(0)
        self.network_interfaces_combo.pack(anchor=W, fill=X)

        self.saveddevs_frame = Frame(self, bg='#333')
        self.saveddevs_frame.pack(fill=BOTH, expand=True)
        self.saveddevs_treeview_cols = ("dev_name", "manufacturer", "model", "mac_addr")
        self.saveddevs_treeview = ttk.Treeview(self.saveddevs_frame, columns=self.saveddevs_treeview_cols, show="headings")
        self.saveddevs_treeview.heading('dev_name', text="Device Name")
        self.saveddevs_treeview.heading('manufacturer', text="Manufacturer")
        self.saveddevs_treeview.heading('model', text="Model")
        self.saveddevs_treeview.heading('mac_addr', text="Mac Address")
        self.saveddevs_treeview.pack(fill=BOTH,expand=True)
        self.saveddevs_treeview.bind('<<TreeviewSelect>>', self.onclick_saved_dev)

        # another frame holding other widgets.
        self.second_frame = Frame(self)
        self.second_frame.pack(fill=BOTH, expand=False)

        self.saveddevs_man_btns_frame = Frame(self.second_frame)
        self.saveddevs_man_btns_frame.pack(fill=X, expand=False)
        self.add_new_saved_dev_btn = ttk.Button(self.saveddevs_man_btns_frame, text="Add new device", command=startSaveNewDeviceWindow)
        self.add_new_saved_dev_btn.pack(anchor=W, expand=True, ipady=4, fill=X, side=LEFT)
        self.remove_saved_dev_btn = ttk.Button(self.saveddevs_man_btns_frame, text="Delete Selected", command=delete_selected_saved_device)
        self.remove_saved_dev_btn.pack(anchor=CENTER, expand=True, ipady=4, fill=X, side=LEFT)
        self.refresh_saved_dev_btn = ttk.Button(self.saveddevs_man_btns_frame, text="Refresh", command=read_from_csv_save)
        self.refresh_saved_dev_btn.pack(anchor=E, expand=True, ipady=4, fill=X, side=LEFT)
        # self.space0 = Label(self, background='#333', text='', font=("Arial", 12)).pack(side=LEFT, fill=X, expand=True)
        self.lbl3 = Label(self.second_frame, text="Enter Device's Mac Address :", font=("Arial", 11), foreground='black').pack(anchor=W)
        self.lbl4 = Label(self.second_frame, text="(valid formats are: XX:XX:XX:XX:XX:XX, XX.XX.XX.XX.XX.XX, XX-XX-XX-XX-XX-XX, XXXXXXXXXXXX)", font=("Arial", 11), foreground='black').pack(anchor=W)
        self.macaddress_entry = ttk.Entry(self.second_frame)
        self.macaddress_entry.pack(anchor=W, fill=X)
        # self.space1 = Label(self, text='', background='#333', foreground='white', font=("Arial", 12)).pack(fill=X, expand=True, side=LEFT)
        self.lbl5 = Label(self.second_frame, text="Choose Magic Packet Port:", font=("Arial", 11), foreground='black').pack(anchor=W)
        self.port_combobox = ttk.Combobox(self.second_frame)
        self.port_combobox['values'] = ("Port 7", "Port 9 (Recommended)")
        self.port_combobox.current(1)
        self.port_combobox.pack(anchor=W, fill=X, pady=5)
        # self.space2 = Label(self.second_frame, text='', font=("Arial", 12), background='#333', foreground='white').pack(anchor=W)
        # Grid.columnconfigure(self, 0, weight=1)
        self.send_wol_packet_btn = ttk.Button(self.second_frame, text="Wake Device using Lan", command=wake_on_lan)
        self.send_wol_packet_btn.pack(anchor=W, ipady=20, side=LEFT, fill=X, expand=True)
        read_from_csv_save()
        # self.send_wol_packet_btn.pack(fill=X, expand=True)
    
    def onclick_saved_dev(self, event):
        """
        Inserts the Mac Address of the selected Saved device from the list for use with sending WoL packets to
        """
        try:
            for selected_item in self.saveddevs_treeview.selection():
                item = self.saveddevs_treeview.item(selected_item)
                dev_mac = str(item['values'][3]).replace('\n', '')
                print(f"[DEBUG]: Inserting mac address: {dev_mac} into the mac address insert widget")
                # let's clear the area first.
                self.macaddress_entry.delete(0, END)
                # now let's insert the device's mac address:
                self.macaddress_entry.insert(END, dev_mac)
        except:
            pass
        return None
        

def print_greeting():
    """
    Prints the greeting text.
    """
    print('=========================================================')
    print("MegaWake for x86_64-based PCs (Windows and Linux Computers)")
    print("Copyright (C) 2022 - 2023 - Ziad Ahmed (Mr.X) aka. Insertx2k Dev")
    print('', end='\n')
    print("This program is a free and open-source product, which means, you are allowed to redistribute it or modify it under the terms of the GNU General Public License v2.0 or later @ Free Software Foundation")
    print('=========================================================')
    print("Running in Command Line mode")
    return None

def print_help_text():
    print_greeting()
    print("""usage: megawake.exe or <megawake filename>.exe [device mac address you want to wake] (--list-interfaces) (network_interface) (wol_port 7|9)
Details:

Required arguments/parameters are:

[device mac address you want to wake] - Is a required argument (or parameter) that represents the string that contains the Mac Address of the device you want to Wake up using Wake on Lan feature.
(valid formats are: XX:XX:XX:XX:XX:XX, XX.XX.XX.XX.XX.XX, XX-XX-XX-XX-XX-XX, XXXXXXXXXXXX)

Optional arguments/parameters are:
'--list-interfaces' - used to show a list of all available network controller interfaces and their local IP and Mac addresses.
(network_interface) - is the local IP address of the network interface you want to use to send a Wake on Lan (WoL) packet (ex. 192.168.1.3)
* if network_interface is not specified, the program will automatically default to the first detected network interface (which is the onboard ethernet controller for most PCs, eth0 for Linux-based computers)
(wol_port 7|9) - Can either be 7 or 9, depends on which port you want to use to send the Wake on Lan (WoL) magic packet (port 9 is recommended as it works for most devices)

Examples of megawake Usage:
megawake.exe 99:22:66:11:3D:C3 192.168.1.6 7
megawake.exe 99:22:66:11:3D:C3 192.168.1.6
megawake.exe 99:22:66:11:3D:C3
megawake.exe --list-interfaces
""")
    return None

def list_network_interfaces():
    print('', end='\n')
    print("Available network interfaces for this system are:")
    for network_interface in network_interfaces:
        print(f"{network_interface}")
    
    return None

def send_wol_packet_from_cmdline(macaddr, network_interface=None, wol_port=9):
    global network_interfaces, network_interfaces_local_ips
    if network_interface != None:
        pass
    else:
        network_interface = network_interfaces_local_ips[0]
    try:
        send_magic_packet(macaddr, interface=network_interface, port=wol_port)
        print(f"{Fore.GREEN}{Style.BRIGHT}success: sent wol packet to {macaddr} on port {wol_port} using interface {network_interface}")
        raise SystemExit(0)
    except Exception as send_wol_packet_error:
        print(f"{Fore.RED}{Style.BRIGHT}error: can't send wol packet due to an error: {send_wol_packet_error}")
        raise SystemExit(15) # exit code 15 is for unable to send wol packet.

if __name__ == '__main__':
    os.chdir(application_path)
    try:
        for network_controller in net_if_addrs():
            # print(f"Network Controller: {network_controller}, Mac Address: {net_if_addrs()[network_controller][0][1]}, Local IP Address: {net_if_addrs()[network_controller][1][1]}") # for mac address in format XX-XX-XX-XX-XX-XX
            # for network controller local ip address i.e. 192.168.1.6
            network_interfaces.append(f"Network Controller: {network_controller}, Mac Address: {net_if_addrs()[network_controller][0][1]}, Local IP Address: {net_if_addrs()[network_controller][1][1]}")
            network_interfaces_local_ips.append(net_if_addrs()[network_controller][1][1])
    except Exception as mwLaunchError:
        error_window.ErrorWindow(errorText=f"\nUnable to retrieve a list of all avaiable network adapters\n{mwLaunchError}")
        # raise SystemExit(300)

    if len(argv) == 1: # program started manually.
        hideConsole() # disables the console window because the program is currently running in GUI mode.
        process = MainWindow().mainloop()
        showConsole()
        raise SystemExit(0)
    else: # program is running in command line mode.
        # showConsole() # re-enables the console window because the program is currently running in command line mode.
        if str(argv[1]) == "--help":
            print_help_text()
            raise SystemExit(0)
        elif str(argv[1]) == "-h":
            print_help_text()
            raise SystemExit(0)
        elif str(argv[1]) == "/?":
            print_help_text()
            raise SystemExit(0)
        elif str(argv[1]) == "--list-interfaces":
            print_greeting()
            list_network_interfaces()
            raise SystemExit(0)
        else:
            if len(argv) == 2:
                print_greeting()
                send_wol_packet_from_cmdline(str(argv[1]))
            elif len(argv) == 3:
                print_greeting()
                send_wol_packet_from_cmdline(str(argv[1]), network_interface=str(argv[2]))
            elif len(argv) == 4:
                print_greeting()
                if int(argv[3]) == 7:
                    send_wol_packet_from_cmdline(str(argv[1]), network_interface=str(argv[2]), wol_port=7)
                if int(argv[3]) == 9:
                    send_wol_packet_from_cmdline(str(argv[1]), network_interface=str(argv[2]), wol_port=9)
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}error: unsupported port number {argv[3]}!, either ports 7 or 9 are allowed.")
                    raise SystemExit(25) # exit code 25 is for unsupported port number.
            else:
                print_greeting()
                print(f"{Fore.YELLOW}{Style.BRIGHT}warning: unnecessary arguments/parameters passed, do '--help' next time for command line usage information")
                if int(argv[3]) == 7:
                    send_wol_packet_from_cmdline(str(argv[1]), network_interface=str(argv[2]), wol_port=7)
                if int(argv[3]) == 9:
                    send_wol_packet_from_cmdline(str(argv[1]), network_interface=str(argv[2]), wol_port=9)
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}error: unsupported port number {argv[3]}!, either ports 7 or 9 are allowed.")
                    raise SystemExit(25) # exit code 25 is for unsupported port number.
                
            
