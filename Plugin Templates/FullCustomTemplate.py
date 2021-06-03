#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- FullCustomTemplate.py
# This is a plugin template for SmartFrame v2.
# This particular template is fully custom -- you can set your output to whatever image or tile size you'd like.

# Required deps: Pillow, termcolor

# DEVELOPER INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GenerateCard() to change the tile size and pixel density of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# The module will grab the user's colors before running your code. This will be located in COLORS
# The user's font is located in SMARTFRAMEFOLDER + "/Fonts/font1.ttf".
# Use the global variable SMARTFRAMEFOLDER for a string with the location of the SmartFrame folder.
# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color of text) if you need to print. 
# If you need to throw an error, use logError("main error description", "more detailed traceback / traceback.format_exc()", sourcename)
# The above will log to both console and the standard error logging file.

# Edit the PIL 'image' variable in GenerateCard in any way that you like! The end result of the variable will be what appears in SmartFrame.
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
def GenerateCard():
	tilesX = 4 # Change this to change tile size
	tilesY = 2 # Change this to change tile size
	dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
	alttext = ""
	imagedraw = ImageDraw.Draw(image)                 
	
	# Your code here
	
	return image, alttext, tilesX, tilesY
#### YOUR CODE HERE ####


def printC(string, color = "white"):
	from termcolor import colored
	print(sourcename + " | " + colored(str(string), color))

def GetPresets():
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
			
GetPresets()
from ErrorLogger import logError
### SmartFrame.py calls this to get a card. I don't recommend editing this.
def GetCard():

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
		
		from Card import Card
		return Card(outputLocation, alttext, sourcename, tilesX, tilesY)
	else:
		# No cards
		printC("No cards to return!...", "red")
		return None
	
if __name__ == "__main__":
	GetCard()
	