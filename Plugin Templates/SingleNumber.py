#!/bin/python3
# RaddedMC's SmartFrame v2 -- SingleNumber.py
# This is a plugin template for SmartFrame v2.
# This particular template will let you show a single large number and some small text with a fancy background.

# Required deps: Pillow, termcolor

# DEVELOPER INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GetCardData() to change the tile size and pixel density of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# Use the global variable SMARTFRAMEFOLDER for a string with the location of the SmartFrame folder.
# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color of text) if you need to print. 

# Make sure to change the sourcename, count, alttext, and maintext variables!
# count should be an integer greater than or equal to 0.
# If you return set all variables to None (ex, if data can't be found), SmartFrame will display nothing for this Card.

# To test, just run your card in a terminal! The image will appear in your Smartframe/Cards folder. I recommend deleting this file before running SmartFrame again.
# Note that if your plugin crashes, it will not take down the whole SmartFrame process. However, tracebacks will be outputted to the user.

# When you're ready to release to the main repo, place all your code and related files in a folder and place it into Available Plugins/, then make a pull request!

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "Set your card's default sourcename here"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math

SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GetCardData():
    count = 21
    maintext = "Some data"
    alttext = "Whatever you want!"
    
    # Your code here
    
    return count, maintext, alttext
#### YOUR CODE HERE ####

def GenerateCard():
    # EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
    tilesX = 2 # I don't recommend changing these values for this template
    tilesY = 2 # I don't recommend changing these values for this template
    dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
    backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
    textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
    circlesbgcolor = (COLORS[3][0]-10, COLORS[3][1]-10, COLORS[3][2]-10) # Change this to a 3-value tuple to change the background color of your progress meter!
    printC("Counter circles background color is " + str(circlesbgcolor))
    
    imageresx = tilesX*dpifactor
    imageresy = tilesY*dpifactor
    image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
    imagedraw = ImageDraw.Draw(image)                 
    imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)
    
    count, maintext, alttext = GetCardData()
    
    if maintext and alttext:
        maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
        if count < 10: # Don't worry i hate this too
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 50*round(dpifactor/50))
        elif count < 20:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 50*round(dpifactor/50))
        elif count < 100:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 50*round(dpifactor/50))
        elif count < 1000:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 40*round(dpifactor/50))
        elif count < 10000:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 35*round(dpifactor/50))
        elif count < 100000:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 30*round(dpifactor/50))
        else:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 20*round(dpifactor/50))
        
        # Logarithm
        try:
            logAmt = math.log((count),10)
        except ValueError:
            logAmt = 1
        if logAmt == 0:
            logAmt = 1
        printC("LogAmt is " + str(logAmt))
        
        # Top position
        topdivamt = (128/(5*logAmt))
        if topdivamt < 3:
            topdivamt = 3
        counttexttop = imageresx/topdivamt
        
        # Start position
        startdivamt = (2.2*logAmt)+3
        if count < 10:
            startdivamt = 3
        counttextstart = imageresx/startdivamt
        
        printC("Counter scale factors are (" + str(startdivamt) + ", " + str(topdivamt) + ")")
            
        # Circles
        cols = math.ceil(math.sqrt(count))
        rows = round(math.sqrt(count))
        printC("Generating a ("+str(cols)+"x"+str(rows)+") grid of " + str(count) + " circles...")
        
        padding = imageresx/(4*cols)
        size = (imageresx/cols) - padding
        for i in range(0,count):
            col = i % cols
            row = math.floor(i/cols)
            xpos = (padding/2)+(size+padding)*col
            ypos = (padding/2)+(size+padding)*row
            imagedraw.ellipse((xpos, ypos, xpos+size, ypos+size), fill=circlesbgcolor)
        
        imagedraw.text((dpifactor/50,3*imageresy/4), maintext, font=maintextfont, fill=textcolor)
        imagedraw.text((counttextstart, counttexttop), str(count), font=counttextfont, fill=textcolor) # Counter text
    else:
        printC("No data! Sending null data.", "red")
        return None, None, None, None
    
    return image, alttext, tilesX, tilesY



### SmartFrame.py calls this to get a card. I don't recommend editing this.
def GetCard():

    # Set presets
    printC("Getting deps...", "blue")
    currentLocation = os.getcwd().replace('\\', '/')
    nextindex = currentLocation.rfind("/")
    global SMARTFRAMEFOLDER
    if currentLocation.endswith("Plugins") or currentLocation.endswith("Plugin Templates"):
        SMARTFRAMEFOLDER = currentLocation[:nextindex]
    else:
        SMARTFRAMEFOLDER = currentLocation
    printC("SmartFrame is located in " + SMARTFRAMEFOLDER, "green")
    
    sys.path.append(SMARTFRAMEFOLDER)
    from Card import Card
    
    printC("Gathering colors...", "blue")
    colorfile = open(SMARTFRAMEFOLDER + '/Colors.txt', 'r')
    colorfileLines = colorfile.readlines()
    global COLORS
    for line in colorfileLines:
        if "#" in line:
            break
        else:
            COLORS.append((int(line[0:3]), int(line[4:7]), int(line[8:11])))
            printC("Added color " + line[0:3] + " " + line[4:7] + " " + line[8:11] + "!")

    # Generate card...
    printC("Starting card generation...", "blue")
    image, alttext, tilesX, tilesY = GenerateCard() # Calls the above function to get data
    
    # Check if card exists
    if image and alttext and tilesX and tilesY:
        printC("Finished generating card!...", "green")
        
        
        # Setup output location
        outputLocation = SMARTFRAMEFOLDER + "/Cards/" + sourcename + ".png"
        printC("Will output to " + outputLocation, "cyan")
        
        # Save
        image.save(outputLocation)
        printC("Image saved to  " + outputLocation + "!", "green")
        
        return Card(outputLocation, alttext, sourcename, tilesX, tilesY)
    else:
        # No cards
        printC("No cards to return!...", "red")
        return None
    
def printC(string, color = "white"):
    from termcolor import colored
    print(sourcename + " | " + colored(str(string), color))
    
if __name__ == "__main__":
    GetCard()
    