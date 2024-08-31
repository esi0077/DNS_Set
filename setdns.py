
# ░█████╗░██████╗░███╗░░░███╗██╗███╗░░██╗  ███████╗░██████╗███╗░░░███╗░█████╗░██╗██╗░░░░░██╗
# ██╔══██╗██╔══██╗████╗░████║██║████╗░██║  ██╔════╝██╔════╝████╗░████║██╔══██╗██║██║░░░░░██║
# ███████║██████╔╝██╔████╔██║██║██╔██╗██║  █████╗░░╚█████╗░██╔████╔██║███████║██║██║░░░░░██║
# ██╔══██║██╔══██╗██║╚██╔╝██║██║██║╚████║  ██╔══╝░░░╚═══██╗██║╚██╔╝██║██╔══██║██║██║░░░░░██║
# ██║░░██║██║░░██║██║░╚═╝░██║██║██║░╚███║  ███████╗██████╔╝██║░╚═╝░██║██║░░██║██║███████╗██║
# ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝  ╚══════╝╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝╚═╝

#  Github : https://github.com/esi0077
#  copyright : https://www.termsfeed.com/live/f4b97073-c05c-4657-b4f9-79c351c8d410
import os
import sys
import ctypes
import subprocess
import time
import threading
import customtkinter as ctk
from tkinter import Frame

# Predefined DNS settings for each button
DNS_SETTINGS = {
    "Electro": ("78.157.42.100", "78.157.42.101"),
    "Radar Game": ("10.202.10.10", "10.202.10.11"),
    "Shekan": ("178.22.122.100", "185.51.200.2"),
    "quade DNS": ("9.9.9.9", "149.112.112.112"),
    "google DNS": ("8.8.8.8", "8.8.4.4"),
    "Comodo DNS": ("8.26.56.26", "8.20.247.20"),
    "Begzar DNS": ("185.55.226.25", "185.55.226.26"),
    "Open DNS": ("208.67.220.220", "208.67.222.222"),
    "DNS 1": ("185.55.226.26", "185.55.225.25"),
    "DNS 2": ("208.67.222.222", "208.67.220.222"),
    "DNS 3": ("185.231.182.126", "37.152.182.112"),
    "DNS 4": ("79.157.42.100", "109.96.8.51"),
    "DNS 5": ("194.36.174.161", "178.22.122.100"),
    "DNS 6": ("78.157.42.100", "178.22.122.101"),
    "DNS 7": ("37.152.182.112", "0.0.0.0"),
    "DNS 8": ("185.51.200.2", "0.0.0.0"),
    "DNS 9": ("178.22.122.100", "0.0.0.0"),
    "DNS 10": ("185.55.226.26", "185.55.225.25"),
    "DNS 11": ("88.135.36.247", "0.0.0.0"),
    "DNS 12": ("532.63.8.717", "262.84.647.7"),
    "DNS 13": ("109.96.8.51", "7.157.42.101"),
    "DNS 14": ("156.154.70.1", "156.154.71.1"),
    "DNS 15": ("91.239.100.100", "89.233.43.71"),
    "DNS 16": ("208.67.220.200", "208.67.222.222"),
    "DNS 17": ("109.69.8.51", "74.82.42.42"),
    "DNS 18": ("91.239.100.100", "89.233.43.71"),
    "DNS 19": ("91.239.100.100", "89.233.43.71"),
    "DNS 20": ("91.239.100.100", "89.233.43.71"),
    "DNS 21": ("208.67.220.200", "208.67.222.222"),
    "DNS 22": ("109.69.8.51", "0.0.0.0"),
    "DNS 23": ("74.82.42.42", "0.0.0.0"),
    "DNS 24": ("8.8.8.8", "8.8.4.4"),
    "DNS 25": ("4.4.4.4", "4.2.2.2"),
    "DNS 26": ("91.239.100.100", "0.0.0.0"),
    "DNS 27": ("195.46.39.39", "195.46.39.40"),
    "DNS 28": ("10.44.8.8", "8.8.8.8"),
    "DNS 29": ("199.85.127.10", "199.85.126.10"),
    "DNS 30": ("208.67.220.220", "208.67.222.222"),
    "DNS 31": ("77.88.8.8", "77.88.8.1"),
    "DNS 32": ("8.20.247.20", "8.26.56.26")
}

def hide_console():
    """ Hide the console window (Windows specific). """
    try:
        if sys.platform == "win32":
            ctypes.windll.kernel32.SetConsoleTitleW(" ")
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window:
                ctypes.windll.user32.ShowWindow(console_window, 0)  # 0 means hide
    except Exception as e:
        print(f"Failed to hide console window: {e}")

def run_as_admin():
    """ Relaunch the script with administrative privileges if not already running as admin. """
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
    except:
        pass

    # Relaunch the script with admin privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def flush_dns():
    """ Flush the DNS cache. """
    try:
        subprocess.run('ipconfig /flushdns', shell=True, check=True)
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error flushing DNS cache: {e}")

def set_dns_windows_ipv4(preferred_dns, alternate_dns):
    """ Set DNS settings for Windows IPv4. """
    try:
        # Get a list of all network interfaces
        interfaces = subprocess.check_output('netsh interface show interface', shell=True, text=True)
        adapters = [line.split()[-1] for line in interfaces.splitlines() if "Connected" in line]

        # Apply DNS settings to each connected adapter
        for adapter_name in adapters:
            subprocess.run(f'netsh interface ipv4 set dns name="{adapter_name}" static {preferred_dns} primary', shell=True, check=True)
            subprocess.run(f'netsh interface ipv4 add dns name="{adapter_name}" {alternate_dns} index=2', shell=True, check=True)
            print(f"IPv4 DNS servers for {adapter_name} set to: {preferred_dns}, {alternate_dns}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error applying DNS settings: {e}")
        return False

def remove_all_dns():
    """ Remove all DNS settings from all network adapters. """
    try:
        # Get a list of all network interfaces
        interfaces = subprocess.check_output('netsh interface show interface', shell=True, text=True)
        adapters = [line.split()[-1] for line in interfaces.splitlines() if "Connected" in line]

        # Remove DNS settings from each connected adapter
        for adapter_name in adapters:
            subprocess.run(f'netsh interface ipv4 set dns name="{adapter_name}" static none', shell=True, check=True)
            subprocess.run(f'netsh interface ipv4 delete dns name="{adapter_name}" all', shell=True, check=True)
            print(f"Removed all DNS servers from {adapter_name}")
        
        # Update label with success message
        result_label.configure(text="DNS settings have been removed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error removing DNS settings: {e}")
        return False

def ping_dns(dns_ip):
    """ Ping the DNS server to test connectivity. """
    try:
        output = subprocess.check_output(["ping", "-n", "1", dns_ip], stderr=subprocess.STDOUT, universal_newlines=True)
        lines = output.split("\n")
        times = [line.split("time=")[-1].split("ms")[0] for line in lines if "time=" in line]
        if times:
            return f"{times[0]} ms"
        return "No response"
    except subprocess.CalledProcessError:
        return "Ping failed"

def apply_dns_settings(dns_type):
    """ Apply the DNS settings and display ping results. """
    preferred_dns, alternate_dns = DNS_SETTINGS[dns_type]
    
    # Show loading message
    result_label.configure(text="Applying DNS settings. Please wait...")
    app.update_idletasks()

    # Simulate a delay for fake loading
    time.sleep(1)  # Adjust the sleep duration as needed

    success = set_dns_windows_ipv4(preferred_dns, alternate_dns)
    
    if success:
        # Ping to test the DNS connection
        preferred_dns_ping = ping_dns(preferred_dns)
        alternate_dns_ping = ping_dns(alternate_dns)
        
        # Update labels with the ping results
        result_label.configure(
            text=f"DNS settings applied for {dns_type}.\n\n"
                 f"Ping results:\n"
                 f"\nPing: {preferred_dns_ping}\n\n")
    else:
        result_label.configure(
            text=f"Failed to apply DNS settings for {dns_type}.")

def apply_dns_settings_with_loading(dns_type):
    """ Wrapper to apply DNS settings with a loading indicator. """
    # Run the apply_dns_settings function in a separate thread to avoid freezing the UI
    threading.Thread(target=apply_dns_settings, args=(dns_type,)).start()

# Hide console window if running on Windows
hide_console()

# Run the script as administrator if needed
if not ctypes.windll.shell32.IsUserAnAdmin():
    run_as_admin()

# Flush the DNS cache on start
flush_dns()

# Create the main window
app = ctk.CTk()
app.title("DNS Setup")
app.geometry("800x600")

# Prevent resizing
app.resizable(False, False)

# Set custom icon using .ico file
app.iconbitmap("dns.ico")

# Create a frame for DNS buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10, fill='both', expand=True)

# Configure the number of columns and spacing
max_columns = 5
button_spacing = 10

# Create and place DNS buttons
for index, dns_type in enumerate(DNS_SETTINGS):
    row = index // max_columns
    column = index % max_columns
    button = ctk.CTkButton(button_frame, text=f"Set {dns_type}", command=lambda t=dns_type: apply_dns_settings_with_loading(t))
    button.grid(row=row, column=column, padx=button_spacing, pady=button_spacing, sticky='ew')

# Create a frame for the remove DNS button
remove_dns_frame = ctk.CTkFrame(app)
remove_dns_frame.pack(pady=10, fill='x')

# Create a button to remove all DNS settings
remove_dns_button = ctk.CTkButton(remove_dns_frame, text="Remove All DNS", command=remove_all_dns, 
                                 width=200, height=50, fg_color="red", text_color="white")
remove_dns_button.pack(pady=10, padx=5)

# Create a frame for the result label
result_frame = ctk.CTkFrame(app)
result_frame.pack(pady=20, fill='x')

# Create a label to display ping results and loading message
result_label = ctk.CTkLabel(result_frame, text="Select a DNS setting to apply.")
result_label.pack()

# Start the main loop
app.mainloop()
