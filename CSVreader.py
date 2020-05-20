#!/usr/bin/env python3
# INITIALISATIONS
#-------------------------------------------  
import csv
import os
operating = True
# FUNCTIONS
#-------------------------------------------  
def loadsettings(default, currentdir): #loads the settings. Settings[0] is the version number. Settings[1] is the file name.
    pathmod = "/Settings" # encodes the subdirectory
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
    return settings
    
def readcsv(settings, currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",", escapechar="*",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates fiels on commas and uses * as an escape character
    with open(str(settings[1]) + '.csv', newline='') as csvfile: #opens the target filename (value storied in settings[1]
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject: #reads over all rows
            tabledata.append(next(csvobject)) #adds all rows to the 'tabledata' list
    return tabledata 

def invalid(): # returns the 'invalid command' message
    print (' ')
    print ('Invalid command')
    print (' ')
# PROGRAM STARTUP
#-------------------------------------------  
print ("""
CSV READER PROTOTYPE

BY SYDNEY CARDEW

""")
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
print ('Settings imported: ' +str(settings))
print (' ')
# MAIN PROGRAM LOOP
#-------------------------------------------    
while operating: 
    print (' ')
    command = input('Please enter your command: ')
    command = command.upper()
    if command == 'READ':
        print ('Preparing to read file.')
        print (' ')
        input('Please make sure a file named \'' +str(settings[1])+ '.csv\' is present in the same folder as this script. Press enter to continue.')
        print (' ')
        tabledata = readcsv(settings, currentdir) # calls the tabledata function
        print (' ')
        showcommand = input('Would you like to see the data you have imported? Y//N? ')
        showcommand = showcommand.upper()
        print (' ')
        if showcommand == 'Y':
            print(tabledata)
        if showcommand == 'N':
            pass
            
    