#!/bin/python3
# RaddedMC's SmartFrame v2 -- SmallText.py
# This is a plugin template for SmartFrame v2.
# This particular template lets you set 4 lines of text in a 2x2 card or 4x2 card.

# Required deps: Pillow, termcolor

# DEVELOPER INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GenerateCard() to change the tile size and pixel density of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# Use the global variable SMARTFRAMEFOLDER for a string with the location of the SmartFrame folder.
# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color of text) if you need to print. 

# Make sure to change the sourcename, lines 1-4, and alttext variables!

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
    line1 = sourcename
    line2 = "Line 2"
    line3 = "Line 3"
    line4 = "Line 4"
    alttext = "Whatever you want!"
    
    # Your code here
    
    return line1, line2, line3, line4, alttext
#### YOUR CODE HERE ####

def GenerateCard():

    # EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
    tilesX = 2 # Change this to change tile size
    tilesY = 2 # Change this to change tile size
    dpifactor = 200
    # Change this to increase card resolution. Don't go too high!!!
    backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
    textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
    
    imageresx = tilesX*dpifactor
    imageresy = tilesY*dpifactor
    image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
    imagedraw = ImageDraw.Draw(image)                 
    imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)

    line1, line2, line3, line4, alttext = GetCardData()
    
    font = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
    imagedraw.text((dpifactor/50,0), line1, font=font, fill=textcolor)
    printC("Line 1: " + line1)
    imagedraw.text((dpifactor/50,imageresy/4), line2, font=font, fill=textcolor)
    printC("Line 2: " + line2)
    imagedraw.text((dpifactor/50,imageresy/2), line3, font=font, fill=textcolor)
    printC("Line 3: " + line3)
    imagedraw.text((dpifactor/50,3*imageresy/4), line4, font=font, fill=textcolor)
    printC("Line 4: " + line4)
    
    
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
    printC("Finished generating card!...", "green")
    
    
    # Setup output location
    outputLocation = SMARTFRAMEFOLDER + "/Cards/" + sourcename + ".png"
    printC("Will output to " + outputLocation, "cyan")
    
    # Save
    image.save(outputLocation)
    printC("Image saved to  " + outputLocation + "!", "green")
    
    return Card(outputLocation, alttext, sourcename, tilesX, tilesY)
    
def printC(string, color = "white"):
    from termcolor import colored
    print(sourcename + " | " + colored(str(string), color))
    
if __name__ == "__main__":
    GetCard()
    