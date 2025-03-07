import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import ttk
from appdirs import user_data_dir
from datetime import datetime, timedelta
import csv
import glob
import os
import configparser

def last_day(date_str):
    try:
        # Parse the input date string to obtain the month and year
        date_format = '%d.%m.%Y'
        date_obj = datetime.strptime(date_str, date_format)
        year = date_obj.year
        month = date_obj.month

        # Calculate the last day of the next month
        next_month = (month % 12) + 1
        if next_month == 1:
            year += 1

        next_month_first_day = datetime(year, next_month, 1)
        last_day = next_month_first_day - timedelta(days=1)

        # Format and return the last day of the month as a string
        return last_day.strftime(date_format)

    except ValueError:
        return "Invalid date format. Please use 'dd.mm.yyyy'."
    
def first_day(date_str):
    try:
        date_format = '%d.%m.%Y'
        date_obj = datetime.strptime(date_str, date_format)
        first_day = datetime(date_obj.year, date_obj.month, 1)

        return first_day.strftime(date_format)

    except ValueError:
        return "Invalid date format. Please use 'dd.mm.yyyy'."
    
def calendar_week(date_str):
    try:
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%d.%m.%Y')
        
        # Adjust the date to have Monday as the first day of the week
        # Week numbers will range from 1 to 53
        calendar_week = date.isocalendar().week
        
        return str(calendar_week)

    except ValueError:
        return "Invalid date format. Please use 'dd.mm.yyyy'."
    
def weekday(date_str):
    try:
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%d.%m.%Y')
        
        # Define a list of German weekday abbreviations
        weekday_abbreviations = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        
        # Get the weekday (0 for Monday, 1 for Tuesday, ..., 6 for Sunday)
        weekday = date.weekday()
        
        # Return the corresponding abbreviation
        return weekday_abbreviations[weekday]

    except ValueError:
        return "Invalid date format. Please use 'dd.mm.yyyy'."
    
def calendar_day(date_str):
    try:
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%d.%m.%Y')
        
        # Get the calendar day as a string (e.g., "28" for "28.09.2023")
        calendar_day = date.strftime('%d')
        
        return str(calendar_day)  

    except ValueError:
        return "Invalid date format. Please use 'dd.mm.yyyy'."
    
def la_eigen_to_as(la_eigen_str):
    switch_dict = {
        "400": "1", # geleistete Arbeit
        "410": "U", # Urlaub
        "420": "K", # Krank
        "430": "F", # Feiertag
        "195": "SU",# Sonderurlaub
        "402": "S", # geleistete Arbeit in der Schweiz
        "512": "WA" # witterungsbedingter Ausfall
    }

    return switch_dict.get(la_eigen_str, "-")

def select_ini_file():
    global ini_path
    ini_path_obj = askopenfile(initialdir=appdata_path)
    if ini_path_obj is not None:
        ini_path = os.path.normpath(ini_path_obj.name)
        settings_folder_entry.delete(0, tk.END)
        settings_folder_entry.insert(tk.END, ini_path)

        read_config()
        refresh_gui()

def select_input_folder():
    initial_folder = input_folder_entry.get()
    input_folder = os.path.normpath(filedialog.askdirectory(initialdir=initial_folder))
    if input_folder:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(tk.END, input_folder)

def select_output_folder():
    initial_folder = output_folder_entry.get()
    output_folder = os.path.normpath(filedialog.askdirectory(initialdir=initial_folder))
    if output_folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(tk.END, output_folder)

def on_select(event):
    global delim
    selected_value = delimiter_combobox.get()
    if selected_value == ';':
        delim = ';'
    elif selected_value == ',':
        delim = ','
    else:
        delim = ';'

def process_csv(input_file):
    error_displayed = False

    output_file = os.path.join(output_folder, os.path.basename(input_file))
    output_file = os.path.splitext(output_file)[0] + '.txt'

    with open(input_file, 'r') as csv_file, open(output_file, 'w') as txt_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter_combobox.get())
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
    global output_folder; global input_folder
    input_folder = input_folder_entry.get()
    csv_files = glob.glob(input_folder + "/*.csv")


    if not glob.os.path.isdir(input_folder):
        messagebox.showinfo("Error", "The input directory does not exist.")
    elif not csv_files:
        messagebox.showinfo("Error", "No CSV files found in the directory.")
    else:
        output_folder = output_folder_entry.get()
        try:
            os.makedirs(output_folder, exist_ok=True)
        except OSError as e:
            result = messagebox.askokcancel("Confirmation", "Illegal path to output directory. Save the output inside of the input folder instead?")    
            if result:
                output_folder = input_folder
            else:
                return
        for csv_file in csv_files:
            process_csv(csv_file)
        messagebox.showinfo("Data Processed", "Data processing completed successfully.")

def save_config():
    config['DEFAULT']['header'] = header_text.get("1.0", tk.END).strip()
    config['DEFAULT']['inFolder'] = input_folder_entry.get()
    config['DEFAULT']['outFolder'] = output_folder_entry.get()
    config['DEFAULT']['skip_firstrow'] = str(skip_firstrow.get())
    config['DEFAULT']['pattern'] = pattern_entry.get()
    config['DEFAULT']['delim'] = str(delimiter_combobox.current())

    global ini_path
    ini_path = settings_folder_entry.get()
    try:
        with open(ini_path, 'w') as configfile:
            config.write(configfile)
    except (OSError, IOError) as e:
        messagebox.showerror(f"Error writing to file: {e}")

def read_config():
    if not os.path.exists(ini_path):
        config['DEFAULT'] = {'header': '',
                            'inFolder': '',
                            'outFolder': '',
                            'pattern': '',
                            'skip_firstrow': '1',
                            'delim': '0'}
        with open(ini_path, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(ini_path)

    global header_section 
    header_section= config['DEFAULT']['header']
    global input_folder
    input_folder = config['DEFAULT']['inFolder']
    global output_folder
    output_folder = config['DEFAULT']['outFolder']
    global pattern
    pattern = config['DEFAULT']['pattern']
    global skip_firstrow_value
    skip_firstrow_value = config.getboolean('DEFAULT', 'skip_firstrow', fallback=False) 
    global delim_index
    delim_index = config['DEFAULT']['delim']

def refresh_gui():
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(tk.END, input_folder)

    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(tk.END, output_folder)

    pattern_entry.delete(0, tk.END)
    pattern_entry.insert(tk.END, pattern)

    header_text.delete(1.0, 'end')
    header_text.insert(tk.END, header_section)

def toggle_pattern_state():
    if pattern_state.get():
        pattern_entry.configure(state='normal')
    else:
        pattern_entry.configure(state='readonly')

# Create the main window
window = tk.Tk()
window.title('CSV Processor')
window.geometry('700x430')
window.minsize(600,430)
window.maxsize(900,430)

appdata_path = user_data_dir(appname='CSVProcessor')
os.makedirs(appdata_path, exist_ok=True)
ini_filename = 'settings_default.ini'
ini_path = os.path.join(appdata_path, ini_filename)
config = configparser.ConfigParser()

read_config()

# Create the settings folder label and entry
settings_folder_label = tk.Label(window, text="Settings:", font=("Arial", 12))
settings_folder_label.grid(row=0, column=0, padx=(10,0), sticky="w")

settings_folder_entry = tk.Entry(window, font=("Arial", 10))
settings_folder_entry.grid(row=0, column=1, sticky="we")
settings_folder_entry.insert(tk.END, ini_path)

settings_folder_button = tk.Button(window, text="...", command=select_ini_file, font=("Arial", 10), cursor="hand2")
settings_folder_button.grid(row=0, column=2, padx=(0,10), sticky="e")

# Create the input folder label and entry
input_folder_label = tk.Label(window, text="Input Folder:", font=("Arial", 12))
input_folder_label.grid(row=2, column=0, padx=(10,0), sticky="w")

input_folder_entry = tk.Entry(window, font=("Arial", 10))
input_folder_entry.grid(row=2, column=1, sticky="we")
input_folder_entry.insert(tk.END, input_folder)

input_folder_button = tk.Button(window, text="...", command=select_input_folder, font=("Arial", 10), cursor="hand2")
input_folder_button.grid(row=2, column=2, padx=(0,10), sticky="e")

# Create the output folder label and entry
output_folder_label = tk.Label(window, text="Output Folder:", font=("Arial", 12))
output_folder_label.grid(row=3, column=0, padx=(10,0), sticky="w")

output_folder_entry = tk.Entry(window, font=("Arial", 10))
output_folder_entry.grid(row=3, column=1, sticky="we")
output_folder_entry.insert(tk.END, output_folder)

output_folder_button = tk.Button(window, text="...", command=select_output_folder, font=("Arial", 10), cursor="hand2")
output_folder_button.grid(row=3, column=2, padx=(0,10), sticky="e")

# Create the pattern label and entry
pattern_label = tk.Label(window, text="Pattern:", font=("Arial", 12))
pattern_label.grid(row=4, column=0, padx=(10,0), sticky="w")

pattern_entry = tk.Entry(window, font=("Arial", 10))
pattern_entry.grid(row=4, column=1, sticky="we")
pattern_entry.insert(tk.END, pattern)
pattern_entry.configure(state="disabled")

pattern_state = tk.BooleanVar()
pattern_state.set(False)

pattern_state_check = tk.Checkbutton(window, text='', variable=pattern_state, command=toggle_pattern_state)
pattern_state_check.grid(row=4, column=2, padx=(0,10), sticky='nsew')

# Create the header section label and text area
header_label = tk.Label(window, text="Header Section:", font=("Arial", 12))
header_label.grid(row=5, column=0, padx=(10,5), sticky="wn")

header_text = ScrolledText(window, font=("Arial", 10), height=10)
header_text.grid(row=5, column=1, sticky="we")
header_text.insert(tk.END, header_section)

# Create the save button
save_button = tk.Button(window, text="Save settings", command=save_config, font=("Arial", 12), cursor="hand2")
save_button.grid(row=6, column=1, sticky="e")

# Create the skip first row checkbox
skip_firstrow = tk.BooleanVar(value=skip_firstrow_value)
skip_firstrow_check = tk.Checkbutton(window, text="Skip first row", variable=skip_firstrow, font=("Arial", 12))
skip_firstrow_check.grid(row=6, column=1)

# Create a Combobox widget
delimiter_label = tk.Label(window, text="Delimiter:", font=("Arial", 12))
delimiter_label.grid(row=6, column=0, padx=(10,0), sticky="w")

delimiter_combobox = ttk.Combobox(window, values=[';', ','], width=2,cursor="hand2")
delimiter_combobox.current(delim_index) 
delimiter_combobox.bind("<<ComboboxSelected>>", on_select)
delimiter_combobox.configure(state='readonly')
delimiter_combobox.grid(row=6, column=1, sticky="w")

# Create the process button
process_button = tk.Button(window, text="Process Data", command=process_folders, font=("Arial", 12), bg="green", fg="white", cursor="hand2")
process_button.grid(row=7, column=1, pady="30", sticky="se")

# Configure column 1 to expand when the window is resized
window.columnconfigure(1, weight=1)

window.rowconfigure(0, pad=7)
window.rowconfigure(1, pad=7)
window.rowconfigure(2, pad=7)
window.rowconfigure(3, pad=7)
window.rowconfigure(4, pad=7)
window.rowconfigure(5, pad=7)
window.rowconfigure(6, pad=7)

# Start the main loop
window.mainloop()
