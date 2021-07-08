#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- COVIDTrends.py by @Raminh05
# This is a plugin to display Rate of Change Increases/Decreases for COVID cases in the MLHU + The Province of Ontario
# COVID Data from the Government of Ontario / The Provincial Ministry of Health 

# THIS PLUGIN REQUIRES BOTH
# Required deps: Pillow, termcolor, csv, datetime, requests (deps for this plugin)
# Required files: The COVID-Trends-Icons folder's content

sourcename = "COVIDTrends"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math
from csv import reader
from datetime import datetime
import requests

SMARTFRAMEFOLDER = ""
COLORS = []

### YOUR CODE HERE ###
def GetCardData():
	now = datetime.now()
	date = now.strftime("%Y-%m-%d")
	
	def GetPathWithinNeighbouringFolder(fileWithin, folder):
		file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
		index = file.rfind("/")
		file = file[:index]
		fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
		return fullImagePath
	
	# -- Calculate COVID trend -- #
	def trend_calculator():
		# -- Fetches data from CSV -- #
		# -- Logic to call data fetching function -- #
		printC("Checking CSV", "yellow")
		
			# -- Fetches csv. -- #
		def get_write_data(ontario_csv_url):
			r = requests.get(ontario_csv_url)
			with open(SMARTFRAMEFOLDER + "/ontario_covid.csv", 'wb') as f:
				f.write(r.content)
				f.close()
		
		# Parses and returns dates 
		def dates():
			with open(SMARTFRAMEFOLDER + "/ontario_covid.csv", 'r') as f:
				data = list(reader(f))
				csv_date = [i[0] for i in data[400::]]
				csv_date = csv_date[-1]
				f.close()
				return csv_date
		
		try:
			printC("Attempting to read CSV", "yellow")
			csv_date = dates()
			print(csv_date)
			with open(SMARTFRAMEFOLDER + "/ontario_covid.csv", 'r') as f:
				data = list(reader(f))
				london_cases = [i[16] for  i in data[400::]] # London Case List
				ontario_cases = [i[35] for  i in data[400::]] # Ontario Case List
				f.close()
			if csv_date != date:
				printC("COVID CSV is out of date. Downloading new file...", "yellow")
				get_write_data('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv')
				trend_calculator()
			else:
				printC("Your COVID data is up-to-date!", "green")
		except:
			printC("CSV file not found. Downloading one...", "yellow")
			get_write_data('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv')
			printC("Downloaded CSV file.", "yellow")
			trend_calculator()
			
				
		# -- Differences -- #
		london_diff = int(london_cases[-1]) - int(london_cases[-2]) # Today and Yesterday 
		ontario_diff = int(ontario_cases[-1]) - int(ontario_cases[-2]) # Today and Yesterday

		if london_diff > 0:
			london_diff = "+" + str(london_diff) + " more | London"
		elif london_diff < 0:
			london_diff = str(london_diff) + " less | London"
		elif london_diff == 0:
			london_diff = "*No change | London"
	
		if ontario_diff > 0:
			ontario_diff = "+" + str(ontario_diff) + " more | Ontario"
		elif ontario_diff < 0:
			ontario_diff = str(ontario_diff) + " less | Ontario"
		elif ontario_diff == 0:
			ontario_diff = "*No change | Ontario"

		return london_diff, ontario_diff
	
	trends = trend_calculator()

	groupList = []

	for trend in trends:
		if "-" in trend:
			groupList.append(Group(trend, [Item("Down arrow", GetPathWithinNeighbouringFolder("Arrow-Down.png", "COVID-Trends-Icons"), (128,162,240), bgFillAmt=1.0)]))
		elif "+" in trend:
			groupList.append(Group(trend, [Item("Up arrow", GetPathWithinNeighbouringFolder("Arrow-Up.png", "COVID-Trends-Icons"), (240,128,128), bgFillAmt=1.0)]))
		elif "*" in trend:
			groupList.append(Group(trend, [Item("Zero arrow", GetPathWithinNeighbouringFolder("Arrow-Zero.png", "COVID-Trends-Icons"), (192,192,192), bgFillAmt=1.0)])) # No change in trend
			
	maintext = "COVID Trends"
	alttext = "Whatever you want!"
	
	return groupList, maintext, alttext

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
