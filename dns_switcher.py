import tkinter as tk
from tkinter import ttk
import subprocess
import logging

# Set up logging to a file
logging.basicConfig(filename='dns_switcher.log', level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def set_dns():
    try:
        selected_option = combo.get()
        interface = "Wi-Fi"  # Adjust this if needed
        logging.info(f"Setting DNS for {selected_option}")
        
        if selected_option == "shecan":
            dns1 = "185.51.200.2"
            dns2 = "178.22.122.100"
        elif selected_option == "electro":
            dns1 = "78.157.42.100"
            dns2 = "78.157.42.101"
        else:
            return
        
        subprocess.run(f'netsh interface ip set dns name="{interface}" source=static addr={dns1}', shell=True, check=True)
        subprocess.run(f'netsh interface ip add dns name="{interface}" addr={dns2} index=2', shell=True, check=True)
        status_label.config(text=f"DNS set to {selected_option}")
    except Exception as e:
        logging.error(f"Set DNS failed: {str(e)}")
        status_label.config(text=f"Error: {str(e)}")

def unset_dns():
    try:
        interface = "Wi-Fi"  # Adjust this if needed
        logging.info("Unsetting DNS")
        subprocess.run(f'netsh interface ip set dns name="{interface}" source=dhcp', shell=True, check=True)
        status_label.config(text="DNS cleared")
    except Exception as e:
        logging.error(f"Unset DNS failed: {str(e)}")
        status_label.config(text=f"Error: {str(e)}")

try:
    # Create main window
    root = tk.Tk()
    root.title("DNS Switcher")
    root.geometry("300x200")
    root.configure(bg="#404040")
    root.iconbitmap('app.ico')    # Add this line
    logging.info("GUI initialized")

    # Create custom style for buttons
    style = ttk.Style()
    style.theme_use('default')
    style.configure('Custom.TButton',
                    background='#666666',
                    foreground='white',
                    borderwidth=0,
                    padding=6,
                    font=('Arial', 10))
    style.map('Custom.TButton',
              background=[('active', '#808080')],
              foreground=[('active', 'white')])

    # Create and configure dropdown
    options = ["shecan", "electro"]
    combo = ttk.Combobox(root, values=options, state="readonly")
    combo.set("shecan")
    combo.pack(pady=20)

    # Create buttons
    set_button = ttk.Button(root, text="Set", command=set_dns, style='Custom.TButton')
    set_button.pack(pady=5)

    unset_button = ttk.Button(root, text="Unset", command=unset_dns, style='Custom.TButton')
    unset_button.pack(pady=5)

    # Status label
    status_label = tk.Label(root, text="", bg="#404040", fg="white")
    status_label.pack(pady=20)

    # Start the application
    root.mainloop()

except Exception as e:
    logging.error(f"Application failed to start: {str(e)}")