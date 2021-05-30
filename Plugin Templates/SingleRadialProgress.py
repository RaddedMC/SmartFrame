#!/bin/python3
# RaddedMC's SmartFrame v2 -- FullCustomTemplate.py
# This is a plugin template for SmartFrame v2.
# This particular template will let you set a percentage value to be rendered into a circle and some text.

# Required deps: Pillow, termcolor

# DEVELOPER INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GetCardData() to change the tile size and pixel density of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# Use the global variable SMARTFRAMEFOLDER for a string with the location of the SmartFrame folder.
# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color of text) if you need to print. 

# Make sure to change the sourcename, progress, alttext, and maintext variables!
# progress should be a float out of 1.
# If you return set all variables to None (ex, if data can't be found), SmartFrame will display nothing for this Card.

# To test, just run your card in a terminal! The image will appear in your Smartframe/Cards folder. I recommend deleting this file before running SmartFrame again.
# Note that if your plugin crashes, it will not take down the whole SmartFrame process. However, tracebacks will be outputted to the user.

# When you're ready to release to the main repo, place all your code and related files in a folder and place it into Available Plugins/, then make a pull request!

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "Set your card's default sourcename here"

from PIL import Image, ImageFont, ImageDraw
import os
import sys

SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GetCardData():
    progress = 0.02
    maintext = "Some data"
    alttext = "Whatever you want!"
    
    # Your code here
    
    return progress, maintext, alttext
#### YOUR CODE HERE ####

def GenerateCard():
    # EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
    tilesX = 2 # I don't recommend changing these values for this template
    tilesY = 2 # I don't recommend changing these values for this template
    dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
    backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
    textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
    progressfillcolor = (COLORS[3][0]+50, COLORS[3][1]+50, COLORS[3][2]+50) # Change this to a 3-value tuple to change the color of your progress meter!
    printC("Progress bar fill color is " + str(progressfillcolor))
    progressbgcolor = (COLORS[3][0]-50, COLORS[3][1]-50, COLORS[3][2]-50) # Change this to a 3-value tuple to change the background color of your progress meter!
    printC("Progress bar background color is " + str(progressbgcolor))
    
    imageresx = tilesX*dpifactor
    imageresy = tilesY*dpifactor
    image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
    imagedraw = ImageDraw.Draw(image)                 
    imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)
    
    progress, maintext, alttext = GetCardData()
    
    if maintext and alttext:
        maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
        if progress < 0.1:
            progresstextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 30*round(dpifactor/50))
            progresstexttop = (imageresy/4)-(dpifactor/10)
        else:
            progresstextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
            progresstexttop = 5*imageresy/16
        imagedraw.text((dpifactor/50,3*imageresy/4), maintext, font=maintextfont, fill=textcolor)
        circlepos = [(imageresx/8,(imageresy/8)-(dpifactor/10)),(7*imageresx/8, (7*imageresy/8)-(dpifactor/10))]
        imagedraw.arc(circlepos, start=135, end=45, fill=progressbgcolor, width=round(dpifactor/4)) # Background
        imagedraw.arc(circlepos, start=135, end=(270*progress)+135, fill=progressfillcolor, width=round(dpifactor/4)) # Background
        imagedraw.text(((imageresx/4)+(dpifactor/10), progresstexttop), str(round(progress*100))+"%", font=progresstextfont, fill=textcolor)
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
    