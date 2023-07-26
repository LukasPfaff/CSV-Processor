# CSV-Processor

This program can be used to transfer Data from .csv files to .txt files. It will use a pattern to retrieve select columns from the .csv file and writing them down in the text file by using the eval method on the pattern. 

## Installation

[Python](https://www.python.org/downloads/) is necessary to use/install this Program. While going through the installer make sure to add it to the PATH variable.

The program uses the 'appdirs' module. To install this module open the Windows Powershell and enter following command:
```
pip install appdirs
```

To simply use the script open powershell and navigate to the folder where you saved the CSVProcessor.py file. Run the script using the following command:
```
python CSVProcessor.py
```

To install it so you have a .exe file that you can simply double click and link to desktop etc. i recommend using pyinstaller. You first need to install pyinstaller using the command:
```
pip install pyinstaller
```
Now use the pyinstaller to build the program with this command:
```
pyinstaller --noconsole CSVProcessor.py
```

Inside the just created 'dist' folder will be a folder called 'CSVProcessor'. This folder contains the whole Program and can be copied to wherever you want your installation to be saved. To easily find the TimeExport.exe order the contents of the folder by 'Type' and it will appear at the top.

Optionally you can use the option --onefile when biulding the program. 
```
pyinstaller --noconsole --onefile CSVProcessor.py
```
This will generate a single executable that contains all the dependencies. However this executable takes a rather long time to start.

## Usage

On the Graphical User Interface you have several options:

- select settings file
- select input folder
- select output folder
- change header text
- -select delimiter
- skip first line option

The save button saves these values to the settings file inside the appdata folder (will be created by the program). 

To alter the pattern activate the checkbox next to it. This extra step should prevent accidental changes to the pattern.
The export process will read all .csv files inside the given input folder. For each file a new .txt file with the same name is created inside the output folder. Activate the "skip first line" option if the files contain a header in the first row. 
The default delimiter for csv files is ','. With some language settings (like German) the delimiter of csv files is ';'. Make sure to select the correct delimiter.
The resulting text files always contain the header text at the top. Subsequently each line of the .csv file is written as specified in the pattern.

## Pattern

To access data of a specific column use 
```
row[i]
```
where i is the index of the column.  
**Note:** The first column has index 0.

Python methods can be used inside the pattern. This allows to alter the values. For example to remove dots from a date:
```
row[1].replace('.','')
```
**Note:** While it is useful it is also possible to inject malicious code with this pattern. Because the data processing calls the eval method with this patten as argument always check the pattern before processing data.

Text and characters that should always be the same are written in quotation marks:
```
'text'
```

These fragments can be put together using the + sign:
```
row[3] + ';' + row[5] + '\n'
```
Use the '\n' fragment at the end of the pattern to write each line of the .csv file into a new line in the output file.

## Example usecase

An example would be if the time attendance system of a company stores the date in a .csv file. Their tax consultant can import the data into LODAS from text files if they have a specific format. To create such text files with the data of the .csv files the settings of the settings_example.ini can be used.

## Multiple settings

For different use cases it can be useful to have multiple settings file. Simply Copy the settings file and rename it (settings_usecase.ini). Now you can change the settings for the new use case. Use the settings field to choose which settings file to use.
**Note:** replace usecase with a descriptive term

## Error handling
  
The Program will throw an Error if the pattern tries to read a column of the .csv file that does not exist. If this error occurs check the pattern and make sure it does not read a column number higher than the amount of columns in the .csv file.  
If the pattern is correct and the Error still occurs the .csv file probably does not use the expected delimiter.  
