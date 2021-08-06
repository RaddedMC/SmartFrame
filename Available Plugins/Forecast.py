#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- Forecast.py by @Raminh05
# This is a plugin to display weather forecast for your specified location!

# -- Bugs so Far: -- #
# THE API IN USE REQUIRES GEOCODING! EXPECT LESS-KNOWN LOCATIONS TO HAVE INCORRECT DATA!
# Icon fetching is super inefficient

# Required deps: Pillow, termcolor, wget, requests, json, datetime, calendar

# -- User-definable variables -- # 
sourcename = "Forecast"
OWM_api_key = "b4f6dd2094bdd5048ce9025a901553df"
mapbox_api_key = "pk.eyJ1IjoiY2Fubm9saSIsImEiOiJja21udzZpN3AxeXJmMm9zN3BuZGR3aTE0In0.w62dorEJ-QKwtJSswhRVaQ"
base_url_geocode = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
city_name = "London"
country = "CA"
unit = ""

# -- Initial module imports -- #
from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math
import requests, json # Fetching and parsing API responses 
import traceback # For error-logging

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
	
	global unit
	# -- Checks if user entered a valid unit system -- #
	printC("Checking unit system...", "yellow")
	if unit == "metric":
		printC("Metric detected!", "green")
		pass

	elif unit == "imperial":
		printC("Imperial detected!", "green")
		pass

	else:
		printC("Entered unit system is either non-existent or is invalid! Falling back to metric.", "yellow")
		unit = "metric"
	
	groupList = []
	
	maintext = "Forecast"
	alttext = "Whatever you want!"
	
	complete_url_geo = base_url_geocode + city_name + ".json?country=" + country + "&access_token=" + mapbox_api_key
	

	geo = requests.get(complete_url_geo)
	x_geo = geo.json()

	# -- Attempts to parse geocoding response -- #
	try:
		printC("Attempting to parse geocoding response...", "yellow")
		main_geo_info = x_geo["features"]
		main_cords = main_geo_info[0]["center"]
		longitude = main_cords[0]
		latitude = main_cords[1]
		place_name = main_geo_info[0]["place_name"]
		printC("Sucessfully parsed geocoding response!", "green")
	except:
		logError("MapBox API failed to find your specified location. Exiting process...", "", sourcename)
		print(complete_url_geo) # Debugging purposes 
		exit() # Quits process

	# -- Assembles url to request weather data -- #
	forecast_data_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(latitude) + "&lon=" + str(longitude) + "&exclude=hourly,minutely,current,alerts&units=metric&appid=" + OWM_api_key

	# print(forecast_data_url) # Debugging purposes 

	response = requests.get(forecast_data_url)
	x = response.json()
	forecast = x["daily"]

	# -- Second batch of module imports -- #
	from datetime import datetime # datetime parsing 
	import calendar # For date to weekday conversion 
	import wget # icon fetching 

	# -- For loop to assemble items and groups -- #
	for day in forecast:
		itemList = [] # Resets itemList for every day

		# -- Date variables and conversion -- #
		unix_time = float(day['dt']) 
		datetime_date = datetime.utcfromtimestamp(unix_time) # Converts Unix Timestamp to datetime format
		strdate = datetime_date.strftime('%Y-%m-%d') # Converts datetime value to string

		# -- Weather variables -- #
		try:
			printC("Attempting to parse forecast response...", "yellow")
			max_temp = str(round(day['temp']['max'])) + chr(176) + "C"
			min_temp = str(round(day['temp']['min'])) + chr(176) + "C"
			condition = day['weather'][0]['description'].title()
			icon_url = "http://openweathermap.org/img/wn/" + day['weather'][0]['icon'] + "@2x.png"
			printC("Sucessfully parsed forecast response!", "green")
		except:
			print(forecast_data_url) # debugging purposes 
			logError("OpenWeatherMap failed to find forecast data for your location. Exiting process...", "", sourcename)
			exit()

		# -- Fetches icon -- #
		wget.download(icon_url, GetPathWithinNeighbouringFolder(day['weather'][0]['icon'] + "@2x.png", "Forecast-Icons"))

		# -- Date to day of the week conversion -- #
		day_of_the_week = calendar.day_name[datetime_date.weekday()]

		# -- Writes itemList and appends GroupList -- #
		itemList.append(Item(condition, GetPathWithinNeighbouringFolder(day['weather'][0]['icon'] + "@2x.png", "Forecast-Icons"), (255,255,255), bgFillAmt=1)) # Colour TBD
		groupList.append(Group(day_of_the_week + " " + strdate + "\n" + "High: " + max_temp + " | Low: " + min_temp , itemList))

	# -- Modifies maintext and alttext -- #
	maintext = "Forecast" + "\n" + place_name
	alttext =  "Tomorrow's Forecast: " + groupList[1].groupName 

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
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 13*round(dpifactor/50))
	
		
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
