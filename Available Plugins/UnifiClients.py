#!/usr/bin/python3
# RaddedMC's Unifi plugin for SmartFrame -- UnifiClients.py

# For users of Ubiquiti Unifi, this plugin will show the number of clients connected to your network through your controller.
# Required: A UniFi network setup with a locally hosted controller

# Required deps: Pillow, termcolor, unificontrol

# Setup: Set the below variables to the IP of your controller, the port if you have changed it, and your login information.
# I know storing logins in plaintext is stupid. If more interest arises I will change this!

# Add any user-definable variables here! (API keys, usernames, etc.)

sourcename = "Unifi Controller"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math
import unificontrol

SMARTFRAMEFOLDER = ""
COLORS = []

controllerHostname = "192.168.1.42" # IP address or hostname of your controller
controllerPort = 8443 # Leave if you don't know this
username = ""
password = ""

#### YOUR CODE HERE ####
def GetCardData():
	count = 21
	maintext = "Some data"
	alttext = "Whatever you want!"
	
	try:
		printC("Logging into controller...")
		client = unificontrol.UnifiClient(username=username, password=password, host=controllerHostname, port=controllerPort)
		devices = client.list_clients()
		count = len(devices)
		printC("There are " + str(count) + " clients on the network.")
		for site in client.list_sites():
			if site['name'] == "default":
				maintext = site['desc'] + "\n" + "devices"
				printC("The site name is " + site['desc'])
				break
			maintext = "Unifi\ndevices"
		
		alttext = "There are " + str(count) + " devices on your network."
	except:
		printC("Unknown error. take a look at the traceback!", "red")
		import traceback
		logError("Unknown error. take a look at the traceback!", traceback.format_exc(), sourcename)
		return None, None, None
	
	
	return count, maintext, alttext
#### YOUR CODE HERE ####

def GenerateCard():
	# EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
	tilesX = 2 # I don't recommend changing these values for this template
	tilesY = 2 # I don't recommend changing these values for this template
	dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
	backgroundcolor = (50, 50, 175) # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
	textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
	circlesbgcolor = (40, 40, 165) # Change this to a 3-value tuple to change the background color of your progress meter!
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
		if not count == 0:
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
		
		imagedraw.text((dpifactor/50,5*imageresy/8), maintext, font=maintextfont, fill=textcolor)
		imagedraw.text((counttextstart, counttexttop), str(count), font=counttextfont, fill=textcolor) # Counter text
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

	