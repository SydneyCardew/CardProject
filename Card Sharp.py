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
#CLASSES
#---------------------------------------------------------------
class TransposedFont:
    "Wrapper for writing rotated or mirrored text"

    def __init__(self, font, orientation=None):
        """
        Wrapper that creates a transposed font from any existing font
        object.

        :param font: A font object.
        :param orientation: An optional orientation.  If given, this should
            be one of Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM,
            Image.ROTATE_90, Image.ROTATE_180, or Image.ROTATE_270.
        """
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


def imgmaker(tabledata, filename):  # reads the rules and coordinates the rest of the process
    for w in range(len(tabledata)):
        settings = []
        rulelist = []
        try:
            with open((tabledata[w][10]) + '.txt',
                      "r") as template:  # reads the appropriate layout file, stored in index 10 of each card entry
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
        for y in range(len(rulelist)):
            rulestemp = list(rulelist[y])
            linestructure = ruleparser(rulestemp, tabledata[w])
            downcursor = lineprint(linestructure, downcursor, textset, w, d)
        pathmod = "\Output\\" + (filename)
        path = currentdir + pathmod
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        os.chdir(path)
        decrement = len(str(len(tabledata))) - len(str(w + 1))
        im.save((filename) + ' ' + '0' * decrement + str(w + 1) + '.png')  # saves a file with the appropriate number
        im.close()
        os.chdir(currentdir)


def lineprint(linestructure, downcursor, textset, cardno, d):
    smallfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=22, index=0, encoding='', layout_engine=None)
    biggerfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=28, index=0, encoding='', layout_engine=None)
    headerfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=42, index=0, encoding='', layout_engine=None)
    if linestructure[3] == 'black':
        rvalue, gvalue, bvalue = 0, 0, 0
    elif linestructure[3] == 'red':
        rvalue, gvalue, bvalue, = 181, 20, 20
    elif linestructure[3] == 'green':
        rvalue, gvalue, bvalue, = 20, 181, 47
    elif linestructure[3] == 'blue':
        rvalue, gvalue, bvalue, = 33, 35, 173
    elif linestructure[3] == 'yellow':
        rvalue, gvalue, bvalue, = 235, 222, 52
    if linestructure[0] == 'BLANK':
        downcursor = downcursor + textset[1]
    elif linestructure[0] == 'HLINE':
        padding = textset[2] - textset[0]
        d.line([(textset[0], downcursor - 5), (padding, downcursor - 5)], fill=(0, 0, 0), width=2)
    else:
        if linestructure[1] == '1':
            curfnt = headerfnt
        elif linestructure[1] == '2':
            curfnt = biggerfnt
        elif linestructure[1] == '3':
            curfnt = smallfnt
        textwidth, textheightfull = d.textsize(linestructure[2], font=curfnt)
        junkwidth, textheightx = d.textsize('x', font=curfnt)
        if linestructure[0] == 'center':
            padding = textset[2] - textwidth
            padding = padding // 2
            downpos = downcursor
        elif linestructure[0] == 'center inverse':
            padding = textset[2] - textwidth
            padding = padding // 2
            downpos = downcursor
            curfnt = TransposedFont(font=curfnt, orientation=Image.ROTATE_180)
        elif linestructure[0] == 'left':
            padding = textset[0]
            downpos = downcursor
        elif linestructure[0] == 'right':
            padding = (textset[2] - textwidth) - textset[0]
            downpos = downcursor
        elif linestructure[0] == 'bottomleft':
            padding = border
            downpos = (textset[3] - textset[0]) - textheightx
        elif linestructure[0] == 'bottomright':
            padding = (textset[2] - textwidth) - textset[0]
            downpos = (textset[3] - textset[0]) - textheightx
        elif linestructure[0] == 'bottom':
            padding = textset[2] - textwidth
            padding = padding // 2
            downpos = (textset[3] - textset[0]) - textheightx
        if linestructure[2] == 'cardnumber':
            decrement = 3 - len(str(cardno + 1))
            d.text((padding, downpos), "Card number " + '0' * decrement + str(cardno + 1), font=curfnt,
                   fill=(rvalue, gvalue, bvalue))
        else:
            d.text((padding, downpos), linestructure[2], font=curfnt, align="center", fill=(rvalue, gvalue, bvalue))
        downcursor = downcursor + textheightx
    return downcursor


def ruleparser(rulestemp,
               tabledata):  # this function turns the data from the template into instructions for the lineprint function
    rulemod = 0  # this variable allows interpretation of lines with different lengths, for example smaller and larger font sizes, inversions etc.
    if rulestemp[0] == 'C':
        if rulestemp[1] == 'I':
            alignment = 'center inverse'
            rulemod = rulemod + 1
        else:
            alignment = 'center'
    elif rulestemp[0] == '<':
        alignment = 'left'
    elif rulestemp[0] == '>':
        alignment = 'right'
    elif rulestemp[0] == 'V':
        if rulestemp[1] == '<':
            alignment = 'bottomleft'
            rulemod = rulemod + 1
        if rulestemp[1] == '>':
            alignment = 'bottomright'
            rulemod = rulemod + 1
        else:
            alignment = 'bottom'
    elif rulestemp[0] == '*':
        alignment = 'BLANK'
        setfont = 'BLANK'
        linetext = 'BLANK'
    elif rulestemp[0] == 'H' and rulestemp[1] == 'R':
        alignment = 'HLINE'
        setfont = 'HLINE'
        linetext = 'HLINE'
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

def tableviewer(tabledata):     
    print ('length of data is ' +str(len(tabledata))+ ' rows')
    print (' ')
    for x in range (len(tabledata)):
        print ('row ' +str(x+1) +(tabledata[x]))
        print (' ')
    
# PROGRAM STARTUP
#-------------------------------------------
parser = argparse.ArgumentParser(prog="Card Sharp")
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
else:
    debug = False
tabledata = readcsv(csvname, currentdir)
if debug == True:
    print (tabledata)
if args.text:
    txtmaker(tabledata,filename)
elif args.image:
    imgmaker(tabledata,filename)