#!/bin/python3
# RaddedMC's SmartFrame v2 -- PluginTemplate.py
# This is a plugin template for SmartFrame v2.
# This particular template is fully custom -- you can set your output to whatever image or tile size you'd like.

# Required deps: Pillow, termcolor

# INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GenerateCard() to change the tile size of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# The module will grab the user's colors before running your code. This will be located in COLORS
# The user's font is located in SmartFrameFolder/Fonts/font1.ttf.
# Use the global variable SMARTFRAMEFOLDER for a string with the location of the SmartFrame folder.
# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color in text) if you need to print. 
# Edit the PIL 'image' variable in GenerateCard in any way that you like! The end result of the variable will be what appears in SmartFrame.
# To test, just run your card in a terminal! The image will appear in your Smartframe/Cards folder. I recommend deleting this file before running SmartFrame again.
# Note that if your plugin crashes, it take down the whole SmartFrame process. However, tracebacks will be outputted to the user.

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "Set your card's default sourcename here"

from PIL import Image, ImageFont, ImageDraw
import os
import sys

SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GenerateCard():
    tilesX = 2 # Change this to change tile size
    tilesY = 2 # Change this to change tile size
    image = Image.new("RGB", (tilesX*200, tilesY*200))
    alttext = ""
    
    # Your code here
    
    return image, alttext, tilesX, tilesY
#### YOUR CODE HERE ####



### SmartFrame.py calls this to get a card. I don't recommend editing this.
def GetCard():

    # Set presets
    printC("Getting deps...", "blue")
    currentLocation = os.getcwd().replace('\\', '/')
    nextindex = currentLocation.rfind("/")
    global SMARTFRAMEFOLDER
    SMARTFRAMEFOLDER = currentLocation[:nextindex]
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
    
if __name__ = "__main__":
    GetCard()
    