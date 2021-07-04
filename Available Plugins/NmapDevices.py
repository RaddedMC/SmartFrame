#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- NmapDevices.py
# This plugin uses nmap to get a list of devices on your network. Useful for sysadmins 

# Required deps: Pillow, termcolor, python-nmap
# You may need to install nmap on your machine to use this plugin. See https://nmap.org/ or make an issue on GitHub if you're having problems!

# This plugin will grab your device's local network IP (not the IP address that the angry script kiddie can use to DDoS your internet)
# and scans your subnet (network) to discover other devices on your network -- then places their names into a nice list :)
sourcename = "Nmap Device List"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math
import nmap
import socket

SMARTFRAMEFOLDER = ""
COLORS = []

### YOUR CODE HERE ###
def GetCardData():
	def GetPathWithinNeighbouringFolder(fileWithin, folder):
		file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
		index = file.rfind("/")
		file = file[:index]
		fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
		return fullImagePath
	
	groupList = []
	maintext = ""
	alttext = ""
	
	try:
		printC("Getting nmap...")
		nm = nmap.PortScanner()
		
		printC("Getting scan range...", "blue")
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('10.255.255.255', 1))
		scanRange = s.getsockname()[0] + "/24"
		
		printC("Scanning range " + scanRange + "...", "blue")
		hosts = nm.scan(hosts=scanRange, arguments="-sn --open")
		
		numDevices = len(hosts['scan'])
		printC(str(numDevices) + " devices found!", "green")
		maintext = str(numDevices) + " total devices"
		alttext = "nmap found " + str(numDevices) + " devices on your network."
		
		printC("Shuffling device list...")
		import random
		hostlist = random.shuffle(list(hosts['scan']))
		keys = list(hosts['scan'].keys())
		random.shuffle(keys)
		
		deviceCount = (2*random.randrange(1,4))+1
		printC("Grabbing info for " + str(deviceCount) + " devices...", "cyan")
		
		for host in keys:
			if len(groupList) < deviceCount:
				hostname = hosts['scan'][host]['hostnames'][0]['name']
				ip = host
				try:
					vendor = hosts['scan'][host]['vendor'][hosts['scan'][host]['addresses']['mac']]
				except:
					vendor = None
					printC("Unable to find vendor information for device " + host, "red")
				
				if hostname == None or hostname == "":
					line1 = host
				else:
					line1 = hostname + " -- " + host
				
				if (not vendor == None) and (not vendor == ""):
					line2 = "by " + vendor
				else:
					line2 = ""
				groupList.append(Group(line1 + "\n" + line2, ""))
			else:
				break
	except:
		import traceback
		logError("Unknown error finding devices! Check the traceback for more info...", traceback.format_exc(), sourcename)
		return None, None, None
	
	# Create an Item(name, iconFilePath, backgroundColorTuple, backgroundFillPercentage) for each item
	# Create a Group(name, arrayOfItems) for each group
	# Return a list of Groups to be generated
	# Use GetPathWithinNeighbouringFolder to get icons related to your plugin.
	
	return groupList, maintext, alttext
### YOUR CODE HERE ###



def GenerateCard():
	
	# Get data
	groupList, maintext, alttext = GetCardData()
	
	# If data is present
	if groupList:
		# Calculate card height
		tilesX = 4
		tilesY = math.floor(len(groupList)/2)+1
		printC("There are " + str(len(groupList)) + " groups in this Card. The card is " + str(tilesY) + " units high.", "yellow")
		
		# Stuff
		dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
		imageresx = tilesX*dpifactor
		imageresy = tilesY*dpifactor
		image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
		imagedraw = ImageDraw.Draw(image)
		backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
		maintextcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 20*round(dpifactor/50))
	
		
		imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)
		padding = dpifactor/50
		top = padding
		for group in groupList:
			printC("Getting Image for group " + group.groupName)
			try:
				groupImg = group.Image((round(imageresx-(padding*2)),round(11*dpifactor/24)), dpifactor/10)
			except:
				import traceback
				logError("Unknown error with group " + group.groupName + "! Moving on to next group...", traceback.format_exc(), sourcename)
				continue
			image.paste(groupImg, (round(padding), round(top)), mask = groupImg)
			top += (11*dpifactor/24) + padding
		imagedraw.text((round(padding), round(top)), maintext, fill=maintextcolor, font=maintextfont)
	else:
		printC("No data! Sending null data.", "red")
		return None, None, None, None
	
	return image, alttext, tilesX, tilesY

# Item class in ObjectGroup
class Item:
	itemName = ""
	iconLocation = "" # Icon file path
	bgColor = (0,0,0) # Background color of item
	bgFillAmt = 1 # Percentage (0 - 1) of background filledness, useful to show smart light brightness
	
	def __init__(self, itemName, iconLocation, bgColor, bgFillAmt=1):
		self.itemName = itemName
		self.iconLocation = iconLocation
		self.bgColor = bgColor
		self.bgFillAmt = bgFillAmt
		print("New Item | " + self.itemName + " with icon at " + self.iconLocation + ". " + str(self.bgFillAmt*100) + "% filled background of color " + str(self.bgColor))
	
	# Returns a pretty Item with a rounded-rectangle background
	def Image(self, xyres, cornerrad):
			
		# Create the image of provided size
		image = Image.new(mode="RGBA", size = (xyres, xyres))
		imagedraw = ImageDraw.Draw(image)
		
		# This background changes height based on the fill amount. Useful for smart light brightness or speaker volume.
		imagedraw.rounded_rectangle([(0,0),(xyres,xyres)], fill=(255,255,255,100), radius=cornerrad) # BG
		imagedraw.rounded_rectangle([(0,round(xyres*(1-self.bgFillAmt))),(xyres,xyres)], fill=(round(self.bgColor[0]), round(self.bgColor[1]), round(self.bgColor[2])), radius=round(cornerrad)) # FG
		
		# Overlay the icon
		icon = Image.open(self.iconLocation)
		icon = icon.resize((round(xyres-(xyres/12)), round(xyres-(xyres/12))))
		image.paste(icon, (round(xyres/25), round(xyres/25)), mask=icon)
		
		return image
		
	def __str__(self):
		return "Item object: " + self.itemName + "' with icon at " + self.iconLocation + ". " + str(self.bgFillAmt*100) + "% filled background of color " + str(self.bgColor)
		
# Group class in ObjectGroup
class Group:
	groupName = ""
	itemArray = []

	def __init__(self, groupName, itemArray):
		self.groupName = groupName
		self.itemArray = itemArray

		nameList = ""
		for item in self.itemArray:
			nameList += item.itemName
			nameList += ", "
		print("New ItemGroup | " + self.groupName + " with items " + nameList)

	def Image(self, xyres, cornerrad):
		# Create image of provided size
		image = Image.new(mode="RGBA", size = xyres)
		imagedraw = ImageDraw.Draw(image)

		# Create background
		imagedraw.rounded_rectangle([(0,0),xyres], fill=(0,0,0, 100), radius=cornerrad)

		# Overlay Items
		padding = round(((2*xyres[0]/3)/6)/20)
		imageWidth = round(((2*xyres[0]/3)/6)-(padding*2))
		leftmost = padding
		for item in self.itemArray:
			try:
				itemImage = item.Image(imageWidth, cornerrad)
			except:
				import traceback
				logError("Unknown error with image " + image.imageName + "! Moving on to next image...", traceback.format_exc(), sourcename)
				continue
			image.paste(itemImage, (leftmost, padding), mask=itemImage)
			leftmost += imageWidth+(padding)
		fontscalefactor = 15 / (self.groupName.count("\n")+1)
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", round(fontscalefactor*padding))
		imagedraw.text((leftmost+padding, 0), self.groupName, font=maintextfont, fill=COLORS[1])

		return image

	def __str__(self):
		nameList = ""
		for item in self.itemArray:
			nameList += item.itemName
			nameList += ", "
		print("ItemGroup: " + self.groupName + " with items " + nameList)

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
