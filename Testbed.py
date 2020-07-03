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
from PIL import ImageColor
# FUNCTIONS

def readcsv(csvname, currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",", escapechar="*",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates fiels on commas and uses * as an escape character
    with open(str(csvname) + '.csv', newline='') as csvfile: #opens the target filename (value storied in settings[1]
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject: #reads over all rows
            tabledata.append(row) #adds all rows to the 'tabledata' list
    return tabledata 

def imgmaker(tabledata, filename):
    ruletypes = 4
    for w in range (len(tabledata)):
        if tabledata[w][1] == 'Null':
            settings = []
            rulelist = []
            with open ('Null.txt', "r") as template:
                for line in template:
                    if line.startswith('###'):
                        pass
                    elif line.startswith('+++'):
                        line = line.strip('\n\r')
                        settings = line[3:].split(',')
                    else:
                        rulelist.append(line.strip('\n\r'))      
        if tabledata[w][1] == 'Basic Treasure' or tabledata[w][1] == 'Splendid Treasure' or tabledata[w][1] == 'Astonishing Treasure':
            settings = []
            rulelist = []
            with open ('Treasure.txt', "r") as template:
                for line in template:
                    if line.startswith('###'):
                        pass
                    elif line.startswith('+++'):
                        line = line.strip('\n\r')
                        settings = line[3:].split(',')
                    else:
                        rulelist.append(line.strip('\n\r'))
        if tabledata[w][1] == 'Item':
            settings = []
            rulelist = []
            with open ('Item.txt', "r") as template:
                for line in template:
                    if line.startswith('###'):
                        pass
                    elif line.startswith('+++'):
                        line = line.strip('\n\r')
                        settings = line[3:].split(',')
                    else:
                        rulelist.append(line.strip('\n\r'))
        for x in range (len(settings)):
            settemp = settings[x].split()
            if settemp[0] == 'SIZE':
                width, height = int(settemp[1]), int(settemp[2])
            if settemp[0] == 'BORDER':
                border = int(settemp[1])
            if settemp[0] == 'BACKGROUND':
                rlevel, glevel, blevel = int(settemp[1]), int(settemp[2]), int(settemp[3])
            if settemp[0] == 'VERTICALSPACE':
                vspace = int(settemp[1])
        im = Image.new('RGB', (width,height), color = (rlevel,glevel,blevel))
        d = ImageDraw.Draw(im)    
        textset = [border,vspace,width,height]
        downcursor = border
        for y in range (len(rulelist)):
            rulestemp = list(rulelist[y])
            linestructure = ruleparser(rulestemp,tabledata[w])
            downcursor = lineprint (linestructure, downcursor, textset, w, d)
        pathmod = "\Output\\" + (filename)
        path = currentdir + pathmod
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass    
        os.chdir(path)        
        decrement = len(str(len(tabledata))) - len(str(w+1)) 
        im.save((filename) + ' ' + '0'*decrement + str(w+1) + '.png')
        im.close()
        os.chdir(currentdir)
    
def lineprint(linestructure, downcursor, textset, cardno, d):
    smallfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=22, index=0, encoding='', layout_engine=None)
    biggerfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=28, index=0, encoding='', layout_engine=None)
    headerfnt = ImageFont.truetype(font='CaslonAntique.ttf', size=42, index=0, encoding='', layout_engine=None)
    if linestructure[0] == 'BLANK':
        downcursor = downcursor + textset[1]
    elif linestructure[0] == 'HLINE':
        padding = textset[2]-textset[0]
        d.line([(textset[0],downcursor-5),(padding,downcursor-5)], fill = (0,0,0), width=2)
    else:
        if linestructure[1] == '1':
            curfnt = headerfnt
        elif linestructure[1] == '2':
            curfnt = biggerfnt
        elif linestructure[1] == '3':
            curfnt = smallfnt    
        textwidth, textheightfull = d.textsize(linestructure[2], font = curfnt)
        junkwidth, textheightx = d.textsize('x', font = curfnt)
        if linestructure[0] == 'center':
            padding = textset[2] - textwidth
            padding = padding // 2
            downpos = downcursor
        elif linestructure[0] == 'left':
            padding = textset[0]
            downpos = downcursor
        elif linestructure[0] == 'right': 
            padding = (textset[2] - textwidth) - textset[0]
            downpos = downcursor
        elif linestructure[0] == 'bottomleft':
            padding = border
            downpos = (textset[3]-textset[0]) - textheightx
        elif linestructure[0] == 'bottomright':
            padding = (textset[2] - textwidth) - textset[0]
            downpos = (textset[3] - textset[0])-textheightx
        elif linestructure[0] == 'bottom':   
            padding = textset[2] - textwidth
            padding = padding // 2            
            downpos = (textset[3] - textset[0])-textheightx
        if linestructure[2] == 'cardnumber':
            decrement = 3 - len(str(cardno+1))
            d.text((padding,downpos), "Card number " + '0'*decrement + str(cardno+1), font = curfnt, fill = (0,0,0))
        else:
            d.multiline_text((padding,downpos), linestructure[2], font = curfnt, align = "center", fill = (0,0,0))
        downcursor = downcursor + textheightx
    return downcursor

            
    
def ruleparser(rulestemp,tabledata):
    rulemod = 0
    if rulestemp[0] == 'C':
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
    if rulestemp[1+rulemod] == '~' and rulestemp[2+rulemod] != '~':
        setfont = '1'
    elif rulestemp[1+rulemod] == '~' and rulestemp[2+rulemod] == '~' and rulestemp[3+rulemod] != '~':
        setfont = '2'
    elif rulestemp[1+rulemod] == '~' and rulestemp[2+rulemod] == '~' and rulestemp[3+rulemod] == '~':
        setfont = '3'
    if (rulestemp[-1].isnumeric()):
        linetext = tabledata[int(rulestemp[-1])]
    if rulestemp[-1] == 'M':
        linetext = 'cardnumber'
    linestructure = [(alignment),(setfont),(linetext)] 
    return linestructure     
        

filename = 'test'
currentdir = os.getcwd() # retrieves the current directory in which the CSVreader.py script is running 
tabledata = readcsv('target', currentdir)
imgmaker(tabledata,filename)
print ('length of data is ' +str(len(tabledata))+ ' rows')
print (' ')
for x in range (len(tabledata)):
    print ('row ' +str(x+1),end='') 
    print (tabledata[x])
    print (' ')
print (' ')    
print ('Done!')