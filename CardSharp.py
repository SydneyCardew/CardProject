#!/usr/bin/env python3

# IMPORTS
#-------------------------------------------  
import csv
import os
import errno
import argparse
import configparser
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import date
from datetime import datetime

#CLASSES
#---------------------------------------------------------------
class TransposedFont: #from PIL, used to create upside down text

    def __init__(self, font, orientation=None):
        self.font = font
        self.orientation = orientation  # any 'transpose' argument, or None

    def getsize(self, text, *args, **kwargs):
        w, h = self.font.getsize(text)
        if self.orientation in (Image.ROTATE_90, Image.ROTATE_270):
            return h, w
        return w, h

    def getmask(self, text, mode="", *args, **kwargs):
        im = self.font.getmask(text, mode, *args, **kwargs)
        if self.orientation is not None:
            return im.transpose(self.orientation)
        return im

# FUNCTIONS
#-------------------------------------------
def readcsv(csvname, currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",", escapechar="*",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates files on commas and uses * as an escape character
    with open(str(csvname) + '.csv', newline='') as csvfile: #opens the target filename (value storied in settings[1]
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject: #reads over all rows
            tabledata.append(row) #adds all rows to the 'tabledata' list
    return tabledata 

def txtmaker(tabledata, filename,path): # function that makes text files out of the table data
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass    
    os.chdir(path)
    for x in range (len(tabledata)): # writes the text files
        f = open((filename) + ' ' + str(x+1) + '.txt',"w+")
        f.write('card number ' + str(x+1) + '\n')
        f.write(' ' + '\n')
        for y in range (len(tabledata[x])):
            f.write((tabledata[x][y]) + '\n')
        f.write(' ' + '\n')
        f.write((filename) + ' ' + str(x+1) + '.txt')    
        f.close()

def imgmaker(tabledata, filename,path,configseg):  # reads the rules and coordinates the rest of the process
    for w in range(len(tabledata)):
        settings = []
        rulelist = []
        config = configparser.ConfigParser()  # the following lines extract the text settings from the config file
        config.read('Settings/config.ini')
        layoutfield = config[(configseg)]['layoutfield']
        try:
            with open('Layouts/' + (tabledata[w][int(layoutfield)]) + '.txt',
                      "r") as template:  # reads the appropriate layout file, stored by default in index 10 of each card entry
                for line in template:
                    if line.startswith('###'):  # ignores comments in the layout file
                        pass
                    elif line.startswith('+++'):  # interprets a line beginning '+++' as the card settings
                        line = line.strip('\n\r')
                        settings = line[3:].split(',')
                    else:
                        rulelist.append(line.strip('\n\r'))
        except FileNotFoundError:
            pass
        for x in range(len(settings)):  # extracts the parameters from the settings line
            settemp = settings[x].split()
            if settemp[0] == 'SIZE':  # extracts the width and height
                width, height = int(settemp[1]), int(settemp[2])
            if settemp[0] == 'BORDER':  # extracts the border size
                border = int(settemp[1])
            if settemp[0] == 'BACKGROUND':  # extracts the background colour (stored as an RGB decimal)
                rlevel, glevel, blevel = int(settemp[1]), int(settemp[2]), int(settemp[3])
            if settemp[0] == 'VERTICALSPACE':  # extracts the vertical space, inserted into layouts with '***'
                vspace = int(settemp[1])
        im = Image.new('RGB', (width, height), color=(rlevel, glevel, blevel))
        d = ImageDraw.Draw(im)
        textset = [border, vspace, width, height]
        downcursor = border
        if args.debug: #creates a neat seperator between each card's data in the log file
            log.write('-------' + '\n')
            log.write(' ' + '\n')
        for y in range(len(rulelist)): # draws the card line by line
            rulestemp = list(rulelist[y]) #pulls each line from the rules one by one
            linestructure = ruleparser(rulestemp, tabledata[w])
            downcursor = lineprint(linestructure, downcursor, textset, w, d,configseg)
        try:
            os.makedirs(path)
        except OSError as exc: #handles the error if the directory already exists
            if exc.errno != errno.EEXIST:
                raise
            pass
        os.chdir(path)
        decrement = len(str(len(tabledata))) - len(str(w + 1)) # adds padding to the numbers so that all the file names will be the same length
        im.save((filename) + ' ' + '0' * decrement + str(w + 1) + '.png')  # saves a file with the appropriate number
        im.close()
        os.chdir(currentdir)

def lineprint(linestructure, downcursor, textset, cardno, d,configseg): #this routine prints each individual line according to the data sent to it by ruleparser
    os.chdir(currentdir)
    config = configparser.ConfigParser() # the following lines extract the text settings from the config file
    config.read('Settings/config.ini')
    smallfontid = config[(configseg)]['smallfontid']
    smallfontsize = config[(configseg)]['smallfontsize']
    biggerfontid = config[(configseg)]['biggerfontid']
    biggerfontsize = config[(configseg)]['biggerfontsize']
    headerfontid = config[(configseg)]['headerfontid']
    headerfontsize = config[(configseg)]['headerfontsize']
    smallfnt = ImageFont.truetype(font=(smallfontid), size=int(smallfontsize), index=0, encoding='', layout_engine=None)
    biggerfnt = ImageFont.truetype(font=(biggerfontid), size=int(biggerfontsize), index=0, encoding='', layout_engine=None)
    headerfnt = ImageFont.truetype(font=(headerfontid), size=int(headerfontsize), index=0, encoding='', layout_engine=None)
    black = config[(configseg)]['black']
    red = config[(configseg)]['red']
    green = config[(configseg)]['green']
    blue = config[(configseg)]['blue']
    yellow = config[(configseg)]['yellow']
    if linestructure[3] == 'black': # the following if/elif statements set the colour
        rvalue, gvalue, bvalue, = int(black[0:3]), int(black[4:7]), int(black[8:11])
    elif linestructure[3] == 'red':
        rvalue, gvalue, bvalue, = int(red[0:3]), int(red[4:7]), int(red[8:11])
    elif linestructure[3] == 'green':
        rvalue, gvalue, bvalue, = int(green[0:3]), int(green[4:7]), int(green[8:11])
    elif linestructure[3] == 'blue':
        rvalue, gvalue, bvalue, = int(blue[0:3]), int(blue[4:7]), int(blue[8:11])
    elif linestructure[3] == 'yellow':
        rvalue, gvalue, bvalue, = int(yellow[0:3]), int(yellow[4:7]), int(yellow[8:11])
    if linestructure[0] == 'BLANK':
        downcursor = downcursor + textset[1]
    elif linestructure[0] == 'HLINE': # draws a horizontal rule
        padding = textset[2] - textset[0]
        d.line([(textset[0], downcursor - 5), (padding, downcursor - 5)], fill=(rvalue, gvalue, bvalue), width=2)
    else:
        if linestructure[1] == '1': #these if statements set the font size
            curfnt = headerfnt
        elif linestructure[1] == '2':
            curfnt = biggerfnt
        elif linestructure[1] == '3':
            curfnt = smallfnt
        textwidth, textheightfull = d.textsize(linestructure[2], font=curfnt) #gets the absolute height and width of the text
        junkwidth, textheightx = d.textsize('x', font=curfnt) #gets the x-height of the text
        if linestructure[0] == 'center': #the following if/elif statements deal with the alignment. textset[0] is the border, [2] the total width of the image, [3] the total height
            padding = (textset[2] - textwidth) // 2
            downpos = downcursor
        elif linestructure[0] == 'center inverse':
            padding = (textset[2] - textwidth) // 2
            downpos = downcursor
            curfnt = TransposedFont(font=curfnt, orientation=Image.ROTATE_180)
        elif linestructure[0] == 'left':
            padding = textset[0]
            downpos = downcursor
        elif linestructure[0] == 'right':
            padding = (textset[2] - textwidth) - textset[0]
            downpos = downcursor
        elif linestructure[0] == 'bottomleft':
            padding = textset[0]
            downpos = (textset[3] - textset[0]) - textheightx
        elif linestructure[0] == 'bottomright':
            padding = (textset[2] - textwidth) - textset[0]
            downpos = (textset[3] - textset[0]) - textheightx
        elif linestructure[0] == 'bottom':
            padding = (textset[2] - textwidth) // 2
            downpos = (textset[3] - textset[0]) - textheightx
        elif linestructure[0] == 'top':
            padding = (textset[2] - textwidth) // 2
            downpos = textset[0]
        elif linestructure[0] == 'topright':
            padding = (textset[2] - textwidth) - textset[0]
            downpos = textset[0]
        elif linestructure[0] == 'topleft':
            padding = textset[0]
            downpos = textset[0]
        if linestructure[2] == 'cardnumber': #prints the card number
            decrement = 3 - len(str(cardno + 1))
            d.text((padding, downpos), "Card number " + ('0' * decrement) + str(cardno + 1), font=curfnt,
                   fill=(rvalue, gvalue, bvalue))
            if args.debug: # logs the card number
                log.write((linestructure[0]) + ' ' + str(rvalue) + ' ' + str(gvalue) + ' ' + str(bvalue) + ' ' + 'Card number ' + ('0' * decrement) + str(cardno+1) + '\n')
                log.write(' ' + '\n')
        else: # writes the line
            d.text((padding, downpos), linestructure[2], font=curfnt, align="center", fill=(rvalue, gvalue, bvalue)) #this line prints the lines of text
            if args.debug: # logs the line
                log.write((linestructure[0]) + ' ' + str(rvalue) + ' ' + str(gvalue) + ' ' + str(bvalue) + ' ' + str(linestructure[2]) + '\n')
                log.write(' ' + '\n')
        downcursor = downcursor + textheightx # this moves the cursor down the image
    return downcursor

def ruleparser(rulestemp,tabledata):  # this function turns the data from the template into instructions for the lineprint function
    rulemod = 0  # this variable allows interpretation of lines with different lengths, for example smaller and larger font sizes, inversions etc.
    if rulestemp[0] == 'C': #the following program of if/elif/else statements logically decomposes the line in the layout file
        if rulestemp[1] == 'I':
            alignment = 'center inverse'
            rulemod += 1
        else:
            alignment = 'center'
    elif rulestemp[0] == '<':
        alignment = 'left'
    elif rulestemp[0] == '>':
        alignment = 'right'
    elif rulestemp[0] == 'V':
        if rulestemp[1] == '<':
            alignment = 'bottomleft'
            rulemod += 1
        if rulestemp[1] == '>':
            alignment = 'bottomright'
            rulemod += 1
        else:
            alignment = 'bottom'
    elif rulestemp[0] == '^':
        if rulestemp[1] == '<':
            alignment = 'topleft'
            rulemod += 1
        if rulestemp[1] == '>':
            alignment = 'topright'
            rulemod += 1
        else:
            alignment = 'top'
    elif rulestemp[0] == '*':
        alignment, setfont, linetext = 'BLANK', 'BLANK', 'BLANK'
    elif rulestemp[0] == 'H' and rulestemp[1] == 'R':
        alignment, setfont, linetext = 'HLINE', 'HLINE', 'HLINE'
    if rulestemp[1 + rulemod] == '~' and rulestemp[2 + rulemod] != '~':
        setfont = '1'
    elif rulestemp[1 + rulemod] == '~' and rulestemp[2 + rulemod] == '~' and rulestemp[3 + rulemod] != '~':
        setfont = '2'
    elif rulestemp[1 + rulemod] == '~' and rulestemp[2 + rulemod] == '~' and rulestemp[3 + rulemod] == '~':
        setfont = '3'
    if (rulestemp[-1].isnumeric()):  # this reads text from the table
        linetext = tabledata[int(rulestemp[-1])]
    elif rulestemp[-1] == 'M':
        linetext = 'cardnumber'
    if rulestemp[-2] == 'R':
        linecolour = 'red'
    elif rulestemp[-2] == 'G':
        linecolour = 'green'
    elif rulestemp[-2] == 'B':
        linecolour = 'blue'
    elif rulestemp[-2] == 'Y':
        linecolour = 'yellow'
    else:
        linecolour = 'black'
    linestructure = [(alignment), (setfont), (linetext), (linecolour)]
    return linestructure

def tableviewer(tabledata,csvname): # logs the data extracted from the CSV for later analysis
    log.write(' ' + '\n')
    for x in range (len(tabledata)):
        log.write('card ' + str(x + 1) + ' ')
        log.write(str(tabledata[x]) + '\n')
        log.write(' ' + '\n')
    log.write ('Card Sharp has detected ' +str(len(tabledata))+ ' card entries in ' +(csvname)+ '.csv')
    log.write(' ' + '\n')

def bl():
    print (' ')
    
# PROGRAM STARTUP
#-------------------------------------------
parser = argparse.ArgumentParser(prog="Card Sharp") # the subsequent lines contain the command line arguments
parser.add_argument("CSV", nargs = '?', help = "The name of the CSV to be read")
parser.add_argument("-d", "--debug", action='store_true', help = "runs in debug mode")
parser.add_argument("-u", "--user", action='store_true', help = "uses user-defined config settings")
group = parser.add_mutually_exclusive_group()
group.add_argument("-t", "--text", action='store_true', help = "produces text output")
group.add_argument("-i", "--image", action='store_true', help = "produces image output")
parser.add_argument("-v","--version", action='version',version='%(prog)s 1.0.0')
args = parser.parse_args()
csvname = args.CSV
currentdir = os.getcwd() # retrieves the current directory in which the CardSharp.py script is running
config = configparser.ConfigParser()
if args.user:
    configseg = 'CURRENT'
else:
    configseg = 'DEFAULT'
config.read('Settings/config.ini')
filename = config[(configseg)]['output']
tabledata = readcsv(csvname, currentdir)
today = str(date.today())
path = currentdir + "\Output\\" + (filename) #Creates the root of the output directory path
increment = 0
while os.path.exists((path) + ' ' + (today) + ' ' + str(increment)):
    increment += 1
path = path + ' ' + today + ' ' + str(increment) #Adds todays date and an increment number to the output directory path
if args.debug: # creates a log file
    now = datetime.now()
    smalltime = now.strftime("%H:%M:%S")
    try:
        os.makedirs((currentdir) + '/Logs/')
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    logincrement = 0
    while os.path.exists((currentdir) + '/Logs/log' + ' ' + (today) + ' ' + str(logincrement) + '.txt'):
        logincrement += 1
    log = open((currentdir) + '/Logs/log' + ' ' + (today) + ' ' + str(logincrement) + '.txt', "w")
    log.write ('Card Sharp Log number ' +str(logincrement)+ '. Date: ' + (today) + '. Time: ' +(smalltime))
    log.write(' ' + '\n')
    log.write(' ' + '\n')
    tableviewer(tabledata,csvname)
if args.text: # makes text files
    bl()
    print ('Card Sharp is creating ' + str(len(tabledata)) + ' txt files in ' +(path)+ ' from ' +(csvname)+ '.csv')
    bl()
    txtmaker(tabledata,filename,path)
    filelist = os.listdir(path)
    if len(filelist) == len(tabledata):
        print ('Card Sharp has successfully created ' + str(len(filelist))+ ' txt files in ' +(path))
    else:
        print ('Unknown error.')
elif args.image: # makes image files
    bl()
    print ('Card Sharp is creating ' + str(len(tabledata)) + ' png files in ' +(path)+ ' from ' +(csvname)+ '.csv')
    bl()
    imgmaker(tabledata,filename,path,configseg)
    filelist = os.listdir(path)
    if len(filelist) == len(tabledata):
        print ('Card Sharp has successfully created ' + str(len(filelist))+ ' png files in ' +(path))
    else:
        print ('Unknown error.')
log.close()