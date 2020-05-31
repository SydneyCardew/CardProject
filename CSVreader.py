#!/usr/bin/env python3
# INITIALISATIONS
#-------------------------------------------  
import csv
import os
import errno
from PIL import Image

operating = True
# FUNCTIONS
#-------------------------------------------  

def loadsettings(default, currentdir): #loads the settings. Settings[0] is the version number. Settings[1] is the file name.
    pathmod = "\\Settings" # encodes the subdirectory
    path = currentdir + pathmod # adds the saving subdirectory to the current directory
    os.chdir(path) # move to the subdirectory
    if default == True: #this condition if the default is to be loaded
        f = open('default.txt', 'r') #opens default
        settings = f.read().splitlines() #reads out to 'settings' variable
        f.close() #closes file
    if default == False: #this condition if the saved options are to be loaded
        f = open('saved.txt', 'r') #opens saved
        settings = f.read().splitlines() #reads out to 'settings' variable
        f.close() #closes file
    print (' ')
    print ('Settings imported.')
    return settings
    
def readcsv(settings, currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",", escapechar="*",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates fiels on commas and uses * as an escape character
    with open(str(settings[1]) + '.csv', newline='') as csvfile: #opens the target filename (value storied in settings[1]
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject: #reads over all rows
            tabledata.append(row) #adds all rows to the 'tabledata' list
    return tabledata 

def invalid(): # returns the 'invalid command' message
    print (' ')
    print ('Invalid command')
    print (' ')
    
def helptext(settings): # prints the help text
    print (' ')
    print ('Available commands in version ' +str(settings[0]))
    print ("""
    
READ - reads a CSV file to the data set
MAKETXT - makes an array of text files from the current data set
MAKEIMG - makes an array of image files from the current data set
VIEW - view the current data set
SETTINGS - change settings options
LOAD - Load settings from a file
SAVE - Save settings to a file
HELP OR ? - Display this text

    """)
    
def txtmaker(tabledata, filename):
    pathmod = "\Output\\" + (filename)
    path = currentdir + pathmod
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass    
    os.chdir(path)
    for x in range (len(tabledata)):
        f = open((filename) + ' ' + str(x+1) + '.txt',"w+")
        f.write('card number ' + str(x+1) + '\n')
        f.write(' ' + '\n')
        for y in range (len(tabledata[x])):
            f.write((tabledata[x][y]) + '\n')
        f.write(' ' + '\n')
        f.write((filename) + ' ' + str(x+1) + '.txt')    
        f.close()    
        
def imgmaker(tabledata, filename):
    os.chdir(currentdir)
    im = Image.new('RGB', (100,100), color=(255,255,255))
    im.save((filename)+'.png')
        
def tableviewer(tabledata):     
    print ('length of data is ' +str(len(tabledata))+ ' rows')
    print (' ')
    for x in range (len(tabledata)):
        print ('row ' +str(x+1) +(tabledata[x]))
        print (' ')
    
# PROGRAM STARTUP
#-------------------------------------------  
print (' ')
print ('CARD MAKER (PROTOTYPE) FOR \'TOO GREEDILY, TOO DEEP\'')
print (' ')
print ('BY SYDNEY CARDEW')
print (' ')
currentdir = os.getcwd() # retrieves the current directory in which the CSVreader.py script is running 
initialisecommand = input('Do you want to import saved options? Y/N? ')
initialisecommand = initialisecommand.upper() # makes input upper case
if initialisecommand == 'Y':
    default = True
if initialisecommand == 'N':
    default = False
if initialisecommand != 'Y' and initialisecommand != 'N': # handles an invalid input
    invalid()
    print ('Proceeding with default settings.')
    print (' ')
    default= False
settings = loadsettings(default, currentdir) #calls the load settings function, which loads the settings from the appropriate file
print (' ')
print ('Version number:' +str(settings[0]))
print (' ')
# MAIN PROGRAM LOOP
#-------------------------------------------    
while operating: 
    print (' ')
    command = input('Please enter your command: ')
    command = command.upper()
    if command == 'READ':
        print (' ')
        print ('Preparing to read file.')
        print (' ')
        input('Please make sure a file named \'' +str(settings[1])+ '.csv\' is present in the same folder as this script. Press enter to continue.')
        print (' ')
        tabledata = readcsv(settings, currentdir) # calls the tabledata function
        havetable = True
        print (' ')
        showcommand = input('Would you like to see the data you have imported? Y/N? ')
        showcommand = showcommand.upper()
        print (' ')
        if showcommand == 'Y':
            print(tabledata)
        if showcommand == 'N':
            pass
    if command == 'VIEW':
        if havetable == False:
            invalid()
        elif havetable == True:
            print (' ')
            tableviewer(tabledata)
    if command == 'MAKETXT':
        if havetable == False:
            invalid()
        elif havetable == True: 
            print (' ')
            filename = input('Please enter a name for your project: ')
            txtmaker(tabledata,filename)
    if command == 'MAKEIMG':
        if havetable == False:
            invalid()
        elif havetable == True: 
            print (' ')
            filename = input('Please enter a name for your project: ')
            imgmaker(tabledata,filename)        
    if command == '?' or command == 'HELP':   
        helptext(settings)
            
    