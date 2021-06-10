#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- Weather.py by @Raminh05
# This is the weather plugin for SmartFrame v2.
# Weather data is provided by OpenWeatherMap
# This particular template lets you set 4 lines of text in a 2x2 card or 4x2 card.

# Required deps for the weather plugin: Pillow, termcolor, requests, wget

# Declare your variables here (e.g. location to get weather data for)
sourcename = "Weather"

owm_api_key = "825400b6f9c8ad02b637fa732cdce498" # up to 60 requests/minute. Feel free to use it for now. I might remove it in the futre. If that's the case, register for your own API key at OpenWeatherMap and replace this one with yours here!
gmaps_api_key = "" # Use the Google Cloud console and Maps Static API to get an API key! Note: Google *does* request payment information to use this API. I recommend using PayPal and keeping your API key and account safe!!
city = "" # Your city/town goes here! REQUIRED!
country_code = "" # Must be ISO 3166-2 code (Tip: Google the ISO 3166-2 for your country) REQUIRED!
unit = "" # metric or imperial only (is cap-sensitive, default is set to metric) (e.g. unit = "metric")


from PIL import Image, ImageFont, ImageDraw
import os
import sys
import requests # For Weather Plugin
import json # For Weather Plugin
import wget # For Image grabbing


SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GetCardData():
	line1 = sourcename
	line2 = "Line 2"
	line3 = "Line 3"
	line4 = "Line 4"
	alttext = "Whatever you want!"
	imagelocation = ""

	#### Weatherdata ####
	global unit
# -- Checks if user entered a valid unit system -- #
	printC("Checking unit system...", "yellow")
	if unit == "metric":
		printC("Metric detected!", "green")
		pass

	elif unit == "imperial":
		pass

	else:
		printC("Entered unit system is either non-existent or is invalid! Falling back to metric.", "yellow")
		unit = "metric"

	# -- Checks if user has entered in the required location parameters. -- #
	import traceback
	if city == "" or country_code == "":
		printC("You didn't enter one or both of the required location parameters! Check city and country_code variables! Returning None to card.", "red") # Throws traceback (hopefully) with grace
		return None, None, None, None, None, None

	else:
		printC("Required parameters are filled in. Attempting to fetch data...", "yellow")
		# -- Weather data gathering -- #
		def assemble_weather_url(owm_api_key, city, country_code, unit): # Assembles url to make a request to
			full_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country_code + "&units=" + unit + "&appid=" + owm_api_key
			return full_url

		def make_request(full_url): #
			response = requests.get(full_url)
			weather_json_data = response.json()
			return weather_json_data

		def parse_response(weather_json_data):
			if weather_json_data["cod"] != "404": # Sucessfuly finds location
				printC("Found the location!", "green")

				# -- Parsing the json -- #
				y = weather_json_data["main"]
				z = weather_json_data["weather"]
				wind = weather_json_data["wind"]

				condition = z[0]["description"]
				temperature = y["temp"]
				wind_speed = wind["speed"]
				wind_deg = wind["deg"]

				# -- Conditionnal wind direction variable -- #
				wind_dir = ""
				if wind_deg == 0:
					wind_dir = "N"
				elif wind_deg == 90:
					wind_dir = "E"
				elif wind_deg == 180:
					wind_dir = "S"
				elif wind_deg == 270:
					wind_dir = "W"
				elif wind_deg in range(1, 89):
					wind_dir = "NE"
				elif wind_deg in range(91, 179):
					wind_dir = "SE"
				elif wind_deg in range(181, 269):
					wind_dir = "SW"
				elif wind_deg in range(271, 359):
					wind_dir = "NW"

				return condition, temperature, wind_speed, wind_dir # returns all the data from parsing
			else: # If cannot find data, send None to the card
				printC("Cannot find your location. Sending None to card", "red")
				line1 = None
				line2 = None
				line3 = None
				line4 = None
				alttext = None

		OWM_url = assemble_weather_url(owm_api_key, city, country_code, unit) # OpenWeatherMap URL to make a request to
		weather_json_data = make_request(OWM_url) # Makes the request
		weather_data = parse_response(weather_json_data) # Parse json -> Python-able stuff and returns a data package

		# -- All the weather data -- #
		weather_condition = weather_data[0]
		temperature = weather_data[1]
		wind_speed = weather_data[2]
		wind_dir = weather_data[3]
		line1 = "Weather for " + weather_json_data["name"]

		# -- Sets lines to use certain units depending on specified unit system -- #
		if unit == "metric":
			line2 = str(round(temperature)) + chr(176) + "C"
			line4 = "Wind: " + str(round(wind_speed*3.6, 2)) + " km/h " + wind_dir # Edit by RaddedMC: OpenWeatherMap's API defaults to m/s, converting to km/h
			alttext = "The temperature is " + str(temperature) + chr(176) + "C. The weather condition: " + weather_condition
		else:
			line2 = str(round(temperature)) + chr(176) + "F"
			line4 = "Wind: " + str(wind_speed) + " mph " + wind_dir
			alttext = "The temperature is " + str(temperature) + chr(176) + "F. The weather condition: " + weather_condition

		line3 = str(weather_condition).title()

		#### WeatherImage ####
		printC("Attempting to download map bg image...", "blue")
		if not gmaps_api_key == "":
			try:
				import urllib.parse
				url = "https://maps.googleapis.com/maps/api/staticmap?key=" + urllib.parse.quote(gmaps_api_key)\
				+ "&center=" + urllib.parse.quote(city + ", " + country_code)\
				+ "&zoom=15" + "&format=png"\
				+ "&maptype=roadmap"\
				+ "&style=element:geometry%7Ccolor:0x0f1114&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0xededed&style=element:labels.text.stroke%7Ccolor:0x18191b&style=feature:administrative%7Celement:geometry%7Ccolor:0x757575&style=feature:administrative%7Celement:geometry.fill%7Ccolor:0x262626&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0x707070&style=feature:administrative%7Celement:labels.text.stroke%7Ccolor:0x1a1a1a&style=feature:administrative.country%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.locality%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:landscape.man_made%7Ccolor:0x000000&style=feature:landscape.natural%7Ccolor:0x001906&style=feature:landscape.natural.terrain%7Celement:geometry%7Ccolor:0x333833&style=feature:poi%7Celement:labels%7Cvisibility:off&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Celement:geometry%7Ccolor:0x101e1e&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:poi.park%7Celement:labels.text.stroke%7Ccolor:0x1b1b1b&style=feature:road%7Celement:geometry.fill%7Ccolor:0x396bb7&style=feature:road%7Celement:geometry.stroke%7Ccolor:0x0f1114&style=feature:road%7Celement:labels.text.fill%7Ccolor:0xededed&style=feature:road%7Celement:labels.text.stroke%7Ccolor:0x000000&style=feature:road.highway%7Celement:geometry%7Ccolor:0x51bcd6&style=feature:road.highway%7Celement:geometry.fill%7Ccolor:0x51bcd6&style=feature:road.highway%7Celement:geometry.stroke%7Ccolor:0x0b0b0f&style=feature:road.highway%7Celement:labels.icon%7Cvisibility:off&style=feature:road.highway%7Celement:labels.text.fill%7Ccolor:0xffffff&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0xd1d1d1&style=feature:transit%7Celement:labels.icon%7Cvisibility:off&style=feature:transit%7Celement:labels.text.fill%7Ccolor:0x666666&style=feature:water%7Celement:geometry%7Ccolor:0x011428&style=feature:water%7Celement:labels.text.fill%7Ccolor:0xa3a3a3"\
				+ "&size=800x400"
				imagelocation = wget.download(url, __file__ + "mapimage.jpg")
				printC("Downloaded!", "green")
			except:
				import traceback
				logError("Failed to grab weather image! Check the traceback...", traceback.format_exc(), sourcename)
		else:
			printC("No API key! If you want a background for your image, go to https://developers.google.com/maps/documentation/streetview/cloud-setup !", "red")

		return line1, line2, line3, line4, alttext, imagelocation

def GenerateCard():

	# EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
	tilesX = 4 # Change this to change tile size
	tilesY = 2 # Change this to change tile size
	dpifactor = 200
	# Change this to increase card resolution. Don't go too high!!!
	backgroundcolor = (0, 32, 111) # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
	textcolor = (99, 243, 255) # Change this to a 3-value tuple to change the text colour!

	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGBA", (tilesX*dpifactor, tilesY*dpifactor))
	imagedraw = ImageDraw.Draw(image)

	line1, line2, line3, line4, alttext, imagelocation = GetCardData()

	if imagelocation == "":
		imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)
	else:
		try:
			# Overlay image
			printC("Opening map image...", "blue")
			mapimg = Image.open(imagelocation)
			mapimg = mapimg.resize((imageresx, imageresy))
			image.paste(mapimg, (0,0))

			# Background darken
			overlay = Image.new("RGBA", (imageresx, imageresy))
			overlayDraw = ImageDraw.Draw(overlay)
			overlayDraw.rectangle([(0,0), (imageresx, imageresy)], fill=(0, 0, 0, 100)) # Semitransparent overlay for text contrast
			image = Image.alpha_composite(image, overlay)
			printC("Map image drawn!", "green")
		except:
			import traceback
			logError("Failed to open weather image! Check the traceback...", traceback.format_exc(), sourcename)
			imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)

		try:
			# Delete old image
			printC("Deleting map image " + imagelocation)
			os.remove(imagelocation)
		except:
			import traceback
			logError("Unable to delete map image! Check out the traceback!", traceback.format_exc(), sourcename)

	if line1 and line2 and line3 and line4 and alttext:
		imagedraw = ImageDraw.Draw(image)
		font = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
		imagedraw.text((dpifactor/25,0), line1, font=font, fill=textcolor)
		printC("Line 1: " + line1)
		imagedraw.text((dpifactor/25,imageresy/4), line2, font=font, fill=textcolor)
		printC("Line 2: " + line2)
		imagedraw.text((dpifactor/25,imageresy/2), line3, font=font, fill=textcolor)
		printC("Line 3: " + line3)
		imagedraw.text((dpifactor/25,3*imageresy/4), line4, font=font, fill=textcolor)
		printC("Line 4: " + line4)

		return image, alttext, tilesX, tilesY
	else:
		printC("No data! Sending null data.", "red")
		return None, None, None, None


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
	
