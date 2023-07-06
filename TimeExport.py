import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import csv
import glob
import os
import configparser

def select_input_folder():
    initial_folder = input_folder_entry.get()
    input_folder = filedialog.askdirectory(initialdir=initial_folder)
    if input_folder:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(tk.END, input_folder)

def select_output_folder():
    initial_folder = output_folder_entry.get()
    output_folder = filedialog.askdirectory(initialdir=initial_folder)
    if output_folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(tk.END, output_folder)

def process_csv(input_file):
    output_folder = output_folder_entry.get()
    os.makedirs(output_folder, exist_ok=True)
    error_displayed = False

    output_file = os.path.join(output_folder, os.path.basename(input_file))
    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(input_file, 'r') as csv_file, open(output_file, 'w') as txt_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        if skip_firstrow.get():
            next(csv_reader)  # Skip the header row if present

        txt_file.write(header_text.get("1.0", tk.END).strip() + '\n')

        for row in csv_reader:
            try:
                txt_file.write(eval(pattern_entry.get()))
            except IndexError:
                if not error_displayed:
                    messagebox.showerror("Error", "File doesn not have as many columns. Could not Export Data!")
                    error_displayed = True

def process_folders():
    input_folder = input_folder_entry.get()
    csv_files = glob.glob(input_folder + "/*.csv")

    for csv_file in csv_files:
        process_csv(csv_file)
    print("Processing completed!")

def save_config():
    config['DEFAULT']['header'] = header_text.get("1.0", tk.END).strip()
    config['DEFAULT']['inFolder'] = input_folder_entry.get()
    config['DEFAULT']['outFolder'] = output_folder_entry.get()
    config['DEFAULT']['skip_firstrow'] = str(skip_firstrow.get())

    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)
    print("Config saved!")

# Create the main window
window = tk.Tk()
window.title('CSV Processing')
window.geometry('900x500')

# Read settings from settings.ini file
os.makedirs('settings', exist_ok=True)
config = configparser.ConfigParser()
if not os.path.exists('settings/settings.ini'):
    config['DEFAULT'] = {'header': '',
                         'inFolder': '',
                         'outFolder': '',
                         'pattern': '',
                         'skip_firstrow': '0'}
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read('settings/settings.ini')

header_section = config['DEFAULT']['header']
input_folder = config['DEFAULT']['inFolder']
output_folder = config['DEFAULT']['outFolder']
pattern = config['DEFAULT']['pattern']
skip_firstrow_value = config.getboolean('DEFAULT', 'skip_firstrow', fallback=False)

# Create the input folder label and entry
input_folder_label = tk.Label(window, text="Input Folder:", font=("Arial", 12))
input_folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

input_folder_entry = tk.Entry(window, font=("Arial", 10))
input_folder_entry.grid(row=0, column=1, padx=(0, 5), pady=10, sticky="we")
input_folder_entry.insert(tk.END, input_folder)

input_folder_button = tk.Button(window, text="...", command=select_input_folder, font=("Arial", 10), width=3, height=1, cursor="hand2")
input_folder_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

# Create the output folder label and entry
output_folder_label = tk.Label(window, text="Output Folder:", font=("Arial", 12))
output_folder_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

output_folder_entry = tk.Entry(window, font=("Arial", 10))
output_folder_entry.grid(row=1, column=1, padx=(0, 5), pady=10, sticky="we")
output_folder_entry.insert(tk.END, output_folder)

output_folder_button = tk.Button(window, text="...", command=select_output_folder, font=("Arial", 10), width=3, height=1, cursor="hand2")
output_folder_button.grid(row=1, column=2, padx=(0, 10), pady=10, sticky="e")

# Create the pattern label and entry
pattern_label = tk.Label(window, text="Pattern:", font=("Arial", 12))
pattern_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

pattern_entry = tk.Entry(window, font=("Arial", 10))
pattern_entry.grid(row=2, column=1, padx=(0, 5), pady=10, sticky="we")
pattern_entry.insert(tk.END, pattern)
pattern_entry.configure(state="disabled")

# Create the header section label and text area
header_label = tk.Label(window, text="Header Section:", font=("Arial", 12))
header_label.grid(row=3, column=0, padx=10, pady=10, sticky="n")

header_text = ScrolledText(window, font=("Arial", 10), height=10)
header_text.grid(row=3, column=1, padx=0, pady=10, sticky="we")
header_text.insert(tk.END, header_section)

# Create the save button
save_button = tk.Button(window, text="Save", command=save_config, font=("Arial", 12), cursor="hand2")
save_button.grid(row=5, column=1, padx=10, pady=20, sticky="e")

# Create the skip first row checkbox
skip_firstrow = tk.BooleanVar(value=skip_firstrow_value)
skip_firstrow_check = tk.Checkbutton(window, text="Skip first row", variable=skip_firstrow, font=("Arial", 12))
skip_firstrow_check.grid(row=5, column=1, padx=(0, 10), pady=10, sticky="w")

# Create the process button
process_button = tk.Button(window, text="Export Data", command=process_folders, font=("Arial", 12), bg="green", fg="white", cursor="hand2")
process_button.grid(row=6, column=1, padx=10, pady=20)

# Configure column 1 to expand when the window is resized
window.grid_columnconfigure(1, weight=1)

# Start the main loop
window.mainloop()
