#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- WemoKasaPlugs.py
# This plugin grabs state info from Belkin WeMo and TP-Link Kasa smart plugs on your network.
# No special setup is required, but if you have issues discovering Kasa plugs, set the KasaSubnet variable to your network's broadcast address!
# (Usually 192.168.1.255 or 192.168.0.255 or something else ending in 255)

# Required deps: Pillow, termcolor, pywemo, python-kasa

sourcename = "Kasa and WeMo plugs"
KasaSubnet = "192.168.1.255"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import pywemo
from kasa import Discover
import asyncio

SMARTFRAMEFOLDER = ""
COLORS = []

def GetCardData():
	def GetPathWithinNeighbouringFolder(fileWithin, folder):
		file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
		index = file.rfind("/")
		file = file[:index]
		fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
		return fullImagePath
		
	itemList = []
	maintext = "Kasa | WeMo"
	alttext = "Whatever you want!" # Number of plugs
	
	plugicon = GetPathWithinNeighbouringFolder("outlet.png", "WemoKasaPlugs")
	
	try:
		printC("Getting Wemo Plugs...", "blue")
		wemoplugs = pywemo.discover_devices()
		for wemoplug in wemoplugs:
			try:
				plugname = wemoplug.basicevent.GetFriendlyName()['FriendlyName']
				plugstate = wemoplug.get_state()
				if not plugstate:
					printC("Plug " + plugname + " is off! Skipping...")
					continue
				plugcolor = (66, 245, 117)
				itemList.append(Item(plugname, plugicon, plugcolor, bgFillAmt=1))
			except:
				import traceback
				logError("Unable to get info from a wemo plug!", traceback.format_exc(), sourcename)
				continue
	except:
		import traceback
		logError("Unknown error with WeMo plugs!", traceback.format_exc(), sourcename)
	
	try:
		printC("Getting Kasa Plugs...", "blue")
		if not KasaSubnet or KasaSubnet == "":
			kasaplugs = asyncio.run(Discover.discover())
		else:
			kasaplugs = asyncio.run(Discover.discover(target=KasaSubnet))
		for plugIP in kasaplugs:
			try:
				plugname = kasaplugs[plugIP].alias
				plugstate = kasaplugs[plugIP].is_on
				if not plugstate:
					printC("Plug " + plugname + " is off! Skipping...")
					continue
				plugcolor = (66, 245, 182) # True
				itemList.append(Item(plugname, plugicon, plugcolor, bgFillAmt=1))
			except:
				import traceback
				logError("Unable to get info from a kasa plug!", traceback.format_exc(), sourcename)
				continue
	except:
		import traceback
		logError("Unknown error with Kasa plugs!", traceback.format_exc(), sourcename)
		
	printC("Data collect done!", "green")
	
	return itemList, maintext, alttext


def GenerateCard():
	
	itemList, maintext, alttext = GetCardData()
	if itemList:
		if len(itemList) > 8:
			tilesX = 4
			tilesY = 4
		elif len(itemList) > 4:
			tilesX = 4
			tilesY = 2
		else:
			tilesX = 2
			tilesY = 2
			
		dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
		imageresx = tilesX*dpifactor
		imageresy = tilesY*dpifactor
		image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
		imagedraw = ImageDraw.Draw(image)                 

		# Draw background
		backgroundcolor = (189, 255, 205) # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
		imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)

		# Draw Item tiles
		padding = dpifactor/50
		xcount = 0
		ycount = 0
		for item in itemList:
			printC("Getting image for item " + item.itemName)
			try:
				itemImg = item.Image(round(dpifactor-(2*padding)-round(dpifactor/8)), round(dpifactor/6))
			except:
				import traceback
				logError("Unknown error with image " + item.itemName + "! Moving on to next image...", traceback.format_exc(), sourcename)
				continue
			image.paste(itemImg, (round((dpifactor/(16/tilesX))+padding+(xcount*(dpifactor-(dpifactor/8)))), round(padding+(ycount*(dpifactor-(dpifactor/8))))), mask=itemImg)
			if xcount+1 == tilesX:
				xcount = 0
				ycount += 1
			else:
				xcount += 1
				
		# Draw maintext
		maintextcolor = (0,0,0) # Change this to a 3-value tuple to change the text colour!
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 12*round(dpifactor/50))
		imagedraw.text((round(padding), round(imageresy-(dpifactor/3))), maintext, fill=maintextcolor, font=maintextfont)
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
		icon = icon.resize((round(xyres-(xyres/3)), round(xyres-(xyres/3))))
		image.paste(icon, (round(xyres/6), round(xyres/10)), mask=icon)
		
		# Add itemname text
		itemtextcolor = (0,0,0) # To change the appearance of maintext font, backgrounds, or anything else, head to GenerateCard()!
		itemtextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", round(xyres/8))
		imagedraw.text((cornerrad/2, 4*xyres/5), self.itemName[:11], fill=itemtextcolor, font=itemtextfont)
		
		return image
		
	def __str__(self):
		return "Item object: " + self.itemName + "' with icon at " + self.iconLocation + ". " + str(self.bgFillAmt*100) + "% filled background of color " + str(self.bgColor)

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
	