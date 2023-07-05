# TimeExport

This Program can be used to Transfer Data from .csv files to .txt files. It will use a pattern to retrieve select columns from the .csv file and writing them down in the text file by using the eval method on the pattern. 

## Installation

[Python](https://www.python.org/downloads/) is necessary to use/install this Program. While going through the installer make sure to add it to the PATH variable.

To simply use the script open powershell and navigate to the Folder where you saved the TimeExport.py file. Run the script using the following command:
```
python TimeExport.py
```

To install it so you have a .exe file that you can simply double click and link to desktop etc. i recommend using pyinstaller. You first need to install pyinstaller using the command:
```
pip install pyinstaller
```
Now use the pyinstaller to build the program with this command:
```
pyinstaller --noconsole TimeExport.py
```

Inside the just created 'dist' folder will be a folder called 'TimeExport'. This folder contains the whole Program and can be copied to wherever you want your installation to be saved. To easily find the TimeExport.exe order the contents of the folder by 'Type' and it will appear at the top.

## Usage

On the Graphical User Interface you have several options:

- select input folder
- select output folder
- change header text
- skip first line option

The save button saves these values to the settings.ini file inside the settings folder (will be created by the program).  
The pattern is read from the settings.ini file but is not editable on the GUI to prevent accidental changes. So to pattern needs to be edited inside the settings.ini file.

The export process will read all .csv files inside the given input folder. For each file a new .txt file with the same name is created inside the output folder. Activate the "skip first line" option if the files contain a header in the first row.  
The resulting text files always contain the header text at the top. Subsequently each line of the .csv file is written as specified in the pattern.

## Pattern

Section will be added later

## Multiple settings

For different use cases it can be useful to have multiple settings file. Simply Copy the settings.ini file and rename it (settings_usecase.ini). Now you can change the settings for a new use case. To go back to your original usecase rename the settings.ini and then rename the settings_usecase.ini back to settings.ini.  
**Note:** replace usecase with a descriptive tem

## Error handling
  
The Program will throw an Error if the pattern tries to read a column of the .csv file that does not exist. If this error occurs check the pattern and make sure it does not read a column number higher than the amount of columns in the .csv file.  
If the pattern is correct and the Error still occurs the .csv file probably does not use the expected delimiter. The expected delimiter is ";".  
The option to change the delimiter might be added later.
