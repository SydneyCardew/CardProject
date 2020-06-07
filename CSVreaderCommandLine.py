#!/usr/bin/env python3
# INITIALISATIONS
#-------------------------------------------  
import csv
import os
import errno
import argparse
import configparser
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# FUNCTIONS
#------------------------------------------- 
    
def readcsv(csvname, currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",", escapechar="*",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates fiels on commas and uses * as an escape character
    with open(str(csvname) + '.csv', newline='') as csvfile: #opens the target filename (value storied in settings[1]
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject: #reads over all rows
            tabledata.append(row) #adds all rows to the 'tabledata' list
    return tabledata 

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
    smallfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=12, index=0, encoding='', layout_engine=None)
    biggerfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=14, index=0, encoding='', layout_engine=None)
    headerfnt = fnt1 = ImageFont.truetype(font='CaslonAntique.ttf', size=12, index=0, encoding='', layout_engine=None)
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
        im = Image.new('RGB', (200,300), color = (250,250,250))
        d = ImageDraw.Draw(im)
        textwidth, textheight = d.textsize("Card number " + str(x), font = smallfnt)
        padding1 = 200 - textwidth
        padding1 = padding1 // 2
        decrement = 3 - len(str(x+1))
        d.multiline_text((padding1,260), "Card number " + '0'*decrement + str(x+1), font = smallfnt, align = "center", fill = (0,0,0))
        im.save((filename) + ' ' + '0'*decrement + str(x+1) + '.png')
    im.close()
        
def tableviewer(tabledata):     
    print ('length of data is ' +str(len(tabledata))+ ' rows')
    print (' ')
    for x in range (len(tabledata)):
        print ('row ' +str(x+1) +(tabledata[x]))
        print (' ')
    
# PROGRAM STARTUP
#-------------------------------------------  
parser = argparse.ArgumentParser(prog="Cardmaker")
parser.add_argument("CSV", nargs = '?', help = "The name of the CSV to be read")
parser.add_argument("-o", "--output",  action='store_true', help = "The name of the files to output")
parser.add_argument("-d", "--debug", help = "runs in debug mode.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-t", "--text", action='store_true', help = "produces text output")
group.add_argument("-i", "--image", action='store_true', help = "produces image output")
parser.add_argument('--version', action='version',version='%(prog)s 0.2.0')
args = parser.parse_args()
csvname = args.CSV
currentdir = os.getcwd() # retrieves the current directory in which the CSVreader.py script is running 
filename = 'test'
if args.debug:
    debug = True
tabledata = readcsv(csvname, currentdir)
if debug == True:
    print (tabledata)
if args.text:
    txtmaker(tabledata,filename)
elif args.image:
    imgmaker(tabledata,filename)
        
    




