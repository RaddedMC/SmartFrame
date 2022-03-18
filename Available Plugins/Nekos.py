#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- Nekos.py
# This plugin grabs a photo from https://nekos.life -- be careful visiting this website as it does contain NSFW content.

# Required deps: Pillow, termcolor, nekos.py, wget

import shutil
from PIL import Image, ImageFont, ImageDraw, ImageOps
import os
import sys
import nekos
import random
import requests

SMARTFRAMEFOLDER = ""
COLORS = []

uniqueneko = random.randrange(0,100000) # used to have more than one neko plugin with a very low chance of conflict
sourcename = "Photo " + str(uniqueneko) + " from Nekos.life "

#### YOUR CODE HERE ####
def GetCardData():
	
	global sourcename
	
	def GetPathWithinNeighbouringFolder(fileWithin, folder):
		file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
		index = file.rfind("/")
		file = file[:index]
		fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
		return fullImagePath
	
	
	# Connect to server
	printC("Downloading photo from nekos.life!", "blue")
	try:
		url = nekos.img("neko")
		printC(url)
		output = GetPathWithinNeighbouringFolder("mew"+str(uniqueneko)+".png", "")
		rfile = requests.get(url, stream=True)
		if rfile.status_code == 200:
			with open(output, "wb") as f:
				rfile.raw.decode_content = True
				shutil.copyfileobj(rfile.raw, f)
	except:
		import traceback
		logError("Error connecting to nekos.life! Check the traceback.", traceback.format_exc(), sourcename)
		return None, None, None

	
	# Meta stuff
	background = (255, 163, 163)
	alttext = "neko mew"
	
	return output, background, alttext
#### YOUR CODE HERE ####

def GenerateCard():
	imageFile, background, alttext = GetCardData()
	
	if not imageFile == "" and imageFile:
		try:
			printC("Opening image..." , "blue")
			icon = Image.open(imageFile)
			icon = ImageOps.exif_transpose(icon)
		except:
			import traceback
			logError("Unable to open image! Check the traceback.", traceback.format_exc(), sourcename)
			return None, None, None, None
	else:
		printC("No image! Sending null data.", "red")
		return None, None, None, None
	
	vertical = False
	if icon.size[1] >= icon.size[0]:
		# Tall image
		vertical = True
		printC("Tall photo! " + str(icon.size[0]) + " x " + str(icon.size[1]))
		choice = random.randint(0,1)
		if choice == 0:
			tilesX = 2
			tilesY = 2
		elif choice == 1:
			tilesX = 4
			tilesY = 4
	else:
		# Not tall image
		printC("Not tall photo! " + str(icon.size[0]) + " x " + str(icon.size[1]))
		choice = random.randint(0,2)
		if choice == 0:
			tilesX = 2
			tilesY = 2
		elif choice == 1:
			tilesX = 4
			tilesY = 4
		elif choice == 2:
			tilesX = 4
			tilesY = 2
	
	printC("Card size is " + str(tilesX) + " x " + str(tilesY), "blue")
	
	dpifactor = 300 # Change this to increase card resolution. Don't go too high!!!
	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
	imagedraw = ImageDraw.Draw(image)
	
	if imageFile and background and alttext:
		imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=background)

		width = round(imageresx-(dpifactor/12))
		height = round(imageresy-(dpifactor/12))
		
		printC("Resizing image to " + str(width) + "x" + str(height))
		
		if vertical or (tilesX == 4 and tilesY == 2):
			# Shrink x and y down to width of viewport
			wpercent = (width / float(icon.size[0]))
			hsize = int((float(icon.size[1]) * float(wpercent)))
			icon = icon.resize((width, hsize))
			# crop top and bottom off to height of viewport (centered)
		
		else:
			# Shrink x and y down to height of viewport
			hpercent = (height / float(icon.size[1]))
			wsize = int((float(icon.size[0]) * float(hpercent)))
			icon = icon.resize((wsize, height))
		
		vcentertop = (icon.size[1]/2)-(height/2)
		vcenterbottom = (icon.size[1]/2)+(height/2)
		hcenterleft = (icon.size[0]/2)-(width/2)
		hcenterright = (icon.size[0]/2)+(width/2)
		
		printC("Vertically centered to " + str(vcentertop) + ", " + str(vcenterbottom))
		icon = icon.crop((hcenterleft, vcentertop, hcenterright, vcenterbottom))
		
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
				
		try:
			printC("Deleting photo " + imageFile)
			os.remove(imageFile)
		except:
			import traceback
			logError("Unable to delete image! Check out the traceback!", traceback.format_exc(), sourcename)
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
	