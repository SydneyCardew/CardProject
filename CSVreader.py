#!/usr/bin/env python3

import csv
import os
operating = True

def loadsettings(default, currentdir):
    pathmod = "/Settings" # encodes the subdirectory
    path = currentdir + pathmod # adds the saving subdirectory to the current directory
    direxists = os.path.exists(path) # checks if the saving subdirectory already exists
    if direxists == True: 
        pass
    if direxists == False:    
        os.mkdir(path) # makes the setting subdirectory if it does not exist
    os.chdir(path) # move to the subdirectory
    if default == True:
        f = open('default.txt', 'r')
        settings = f.read().splitlines()
        f.close()
    if default == False:
        f = open('saved.txt', 'r')
        settings = f.read().splitlines()
        f.close()
    return settings
    
def readcsv(settings, currentdir):
    os.chdir(currentdir)
    with open(str(settings[1]) + '.csv', newline='') as csvfile:
        tabledata = csv.reader(csvfile, delimiter=' ', quotechar='|')  
    return tabledata    

def invalid():
    print (' ')
    print ('Invalid command')
    print (' ')


print ("""
CSV READER PROTOTYPE

BY SYDNEY CARDEW

""")

currentdir = os.getcwd() # retrieves the current directory in which the CSVreader.py script is running 
initialisecommand = input('Do you want to import saved options? Y/N? ')
initialisecommand = initialisecommand.upper()
if initialisecommand == 'Y':
    default = True
if initialisecommand == 'N':
    default = False
if initialisecommand != 'Y' and initialisecommand != 'N':
    invalid()
    print ('Proceeding with default settings.')
    print (' ')
    default= False
settings = loadsettings(default, currentdir)
print (' ')
print ('Settings imported: ' +str(settings))
print (' ')
    
while operating:
    print (' ')
    command = input('Please enter your command: ')
    command = command.upper()
    if command == 'READ':
        print ('Preparing to read file.')
        print (' ')
        input('Please make sure a file named \'' +str(settings[1])+ '.csv\' is present in the same folder as this script. Press enter to continue.')
        print (' ')
        tabledata = readcsv(settings, currentdir)
        print (' ')
        showcommand = input('Would you like to see the data you have imported? Y//N? ')
        showcommand = showcommand.upper()
        print (' ')
        if showcommand == 'Y':
            print(tabledata)
        if showcommand == 'N':
            pass
            
    