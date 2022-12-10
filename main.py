"""
MegaWake - A wake on lan program for i486-based Computers (PCs running Windows and Linux Operating Systems)

Licensed under the GNU General Public License v2.0 or later @ Free Software Foundation.

Copyright (C) 2022 - Ziad Ahmed aka. Insertx2k Dev (Mr.X)
"""


# -------------------------
# fixes for pyinstaller when showing console window when gui is launched.
import sys

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
from wakeonlan import send_magic_packet
from psutil import net_if_addrs
from sys import argv, exit
from colorama import Fore, Back, Style, init


# initializing colorama.
init(autoreset=True)

# network interfaces lists.
network_interfaces = []
network_interfaces_local_ips = []

class MainWindow(Tk):
    def __init__(self) -> None:
        global network_interfaces, network_interfaces_local_ips
        super().__init__()
        self.title("megawake")
        self.geometry('750x330')
        # self.minsize(750,600)
        self.resizable(True, True)
        self.configure(background='#333')

        try:
            self.iconbitmap("icon1.ico")
        except Exception as icon_loading_error:
            messagebox.showerror("Window traceback", f"Couldn't load the iconbitmap for this window due to the exception\n{icon_loading_error}")
            pass

        self.lbl0 = Label(self, text="Wake on Lan options:", font=("Arial", 11), foreground='white', background='#333').grid(column=0, row=1, sticky='w')

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

            

        self.lbl2 = Label(self, text="Choose Network Interface:", font=("Arial", 11), foreground='white', background='#333').grid(column=0, row=2, sticky='w')
        self.network_interfaces_combo = ttk.Combobox(self, width=120)
        self.network_interfaces_combo['values'] = network_interfaces
        self.network_interfaces_combo.current(0)
        self.network_interfaces_combo.grid(column=0, row=3, sticky='w')
        self.space0 = Label(self, background='#333', text='', font=("Arial", 12)).grid(column=0, row=4, sticky='w')
        self.lbl3 = Label(self, text="Enter Device's Mac Address :", font=("Arial", 11), foreground='white', background='#333').grid(column=0, row=5, sticky='w')
        self.lbl4 = Label(self, text="(valid formats are: XX:XX:XX:XX:XX:XX, XX.XX.XX.XX.XX.XX, XX-XX-XX-XX-XX-XX, XXXXXXXXXXXX)", font=("Arial", 11), foreground='white', background='#333').grid(column=0, row=6, sticky='w')
        self.macaddress_entry = ttk.Entry(self, width=123)
        self.macaddress_entry.grid(column=0, row=7, sticky='w')
        self.space1 = Label(self, text='', background='#333', foreground='white', font=("Arial", 12)).grid(column=0, row=8, sticky='w')
        self.lbl5 = Label(self, text="Choose Magic Packet Port:", font=("Arial", 11), background='#333', foreground='white').grid(column=0, row=9, sticky='w')
        self.port_combobox = ttk.Combobox(self, width=120)
        self.port_combobox['values'] = ("Port 7", "Port 9 (Recommended)")
        self.port_combobox.current(1)
        self.port_combobox.grid(column=0, row=10, sticky='w')
        self.space2 = Label(self, text='', font=("Arial", 12), background='#333', foreground='white').grid(column=0, row=11, sticky='w')
        self.send_wol_packet_btn = ttk.Button(self, text="Wake Device using Lan", command=wake_on_lan).place(x=112, y=260, relwidth=0.70, relheight=0.16)
        

def print_greeting():
    """
    Prints the greeting text.
    """
    print('=========================================================')
    print("MegaWake for i486-based PCs (Windows and Linux Computers)")
    print("Copyright (C) 2022 - Ziad Ahmed (Mr.X) aka. Insertx2k Dev")
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

    for network_controller in net_if_addrs():
        # print(f"Network Controller: {network_controller}, Mac Address: {net_if_addrs()[network_controller][0][1]}, Local IP Address: {net_if_addrs()[network_controller][1][1]}") # for mac address in format XX-XX-XX-XX-XX-XX
        # for network controller local ip address i.e. 192.168.1.6
        network_interfaces.append(f"Network Controller: {network_controller}, Mac Address: {net_if_addrs()[network_controller][0][1]}, Local IP Address: {net_if_addrs()[network_controller][1][1]}")
        network_interfaces_local_ips.append(net_if_addrs()[network_controller][1][1])

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
                
