#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- 1UnitImage.py
# This is a plugin template for SmartFrame v2.
# This particular template lets you display an icon and a custom background.
# MAKE SURE THAT YOUR ICON IS OBVIOUS -- for example a lightbulb icon could refer to Philips Hue or a hint/tip icon.

# Required deps: Pillow, termcolor

# DEVELOPER INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GetCardData() to change the tile size and pixel density of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# Use the global variable SMARTFRAMEFOLDER for a string with the location of the SmartFrame folder.
# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color of text) if you need to print. 
# If you need to throw an error, use logError("main error description", "more detailed traceback / traceback.format_exc()", sourcename)
# The above will log to both console and the standard error logging file.

# Make sure to change the sourcename, imagePath, background, and alttext variables!

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
	imagePath = "" # File within same folder as plugin (I recommend creating a subfolder with assets related to your plugin
	
	background = (100,0,0) # Red, Green, Blue
	alttext = "Whatever you want!"
	
	# Your code here
	
	file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
	index = file.rfind("/")
	file = file[:index]
	fullImagePath = file + "/" + imagePath # File location of image
	
	fullImagePath = ""
	
	return fullImagePath, background, alttext
#### YOUR CODE HERE ####

def GenerateCard():
	tilesX = 1 # Change this to change tile size
	tilesY = 1 # Change this to change tile size
	dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
	imagedraw = ImageDraw.Draw(image)
	
	imageFile, background, alttext = GetCardData()
	
	if imageFile and background and alttext:
		imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=background)
		try:
			icon = Image.open(imageFile)
		except:
			import traceback
			logError("Unable to open image! Check the traceback.", traceback.format_exc(), sourcename)
			return None, None, None, None
		icon = icon.resize((round(imageresx-(dpifactor/12)), round(imageresy-(dpifactor/12))))
		try:
			image.paste(icon, (round(dpifactor/25), round(dpifactor/25)), mask=icon)
		except:
			printC("Error with transparency! Trying without...", "red")
			try:
				image.paste(icon, (round(dpifactor/25), round(dpifactor/25)))
			except:
				import traceback
				logError("Unable to display image! Check the traceback.", traceback.format_exc(), sourcename)
				return None, None, None, None
	else:
		printC("No data! Sending null data.", "red")
		return None, None, None, None
	
	return image, alttext, tilesX, tilesY


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
	