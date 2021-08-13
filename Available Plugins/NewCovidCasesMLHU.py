#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- NewCovidCasesMLHU.py by @Raminh05
# This is a plugin to display daily new covid cases in the region of Middlesex-London, Ontario, Canada.
# Middlesex-London COVID data from the Government of Ontario

# Required deps for NewCasesMLHUCovid: Pillow, termcolor, requests, datetime, csv (should already be included)

# No need to define any user variables! It just works. 

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "NewCOVIDCasesMLHU"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math

SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GetCardData():
	count = 21
	maintext = "Some data"
	alttext = "Whatever you want!"

	# -- Import modules -- #
	from csv import reader
	import requests
	from datetime import datetime

	now = datetime.now()
	date = now.strftime("%Y-%m-%d")

	# -- Parses and returns case figures -- #
	def cases():
		with open(SMARTFRAMEFOLDER + "/ontario_covid.csv", 'r') as f:
			data = list(reader(f))
			cases = [i[16] for i in data[400::]] # Modifed from NewCovidCasesOntario to suit Middlesex region
			f.close()
			return cases
		
	def dates():
		with open(SMARTFRAMEFOLDER + "/ontario_covid.csv", 'r') as f:
			data = list(reader(f))
			dates = [i[0] for i in data[400::]]
			f.close()
			csv_date = dates[-1]
			return csv_date

   # -- Date and csv currency logi (re-written by @RaddedMC 08/13/21) -- #

	# Check if CSV Exists
		# If yes, run date check
		# If no, download new one

	# If date check successful, continue
	# If date check failed, download new file (unless already downloaded)

	def downloadFile():
		try:
			r = requests.get('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv')
			with open(SMARTFRAMEFOLDER + "/ontario_covid.csv", 'wb') as f:
				f.write(r.content)
				f.close()
		except:
			import traceback
			logError("Unable to download COVID information! Check the traceback.", traceback.format_exc(), sourcename)
			raise ConnectionError

	printC("Checking for a CSV file...", "blue")
	if os.path.isfile(SMARTFRAMEFOLDER + "/ontario_covid.csv"):
		printC("Found a file!", "green")
		csv_date = dates()
		print(csv_date)
		if csv_date != date:
			printC("File is out of date. Downloading a new one.", "red")
			try:
				downloadFile()
			except ConnectionError:
				return None, None
		else:
			printC("File is up to date!", "green")
	else:
		printC("File doesn't exist! Downloading a new one.", "red")
		try:
			downloadFile()
		except ConnectionError:
			return None, None
	
	# -- Fetches information from csv -- #
	case = cases()
	count = int(case[-1])

	maintext = "New\nMiddlesex-London\nCOVID Cases Today" # Spaces to fix centering
	alttext = "There are " + str(count) + " new cases of COVID-19 in Middlesex-London today."

	return count, maintext, alttext
#### YOUR CODE HERE ####

def GenerateCard():
	# EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
	tilesX = 2 # I don't recommend changing these values for this template
	tilesY = 2 # I don't recommend changing these values for this template
	dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
	backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
	textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
	circlesbgcolor = (COLORS[3][0]-10, COLORS[3][1]-10, COLORS[3][2]-10) # Change this to a 3-value tuple to change the background color of your progress meter!
	printC("Counter circles background color is " + str(circlesbgcolor))

	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
	imagedraw = ImageDraw.Draw(image)
	imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)

	count, maintext, alttext = GetCardData()

	if maintext and alttext:
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 10*round(dpifactor/50))
		if count in range(0, 1000): # Don't worry i hate this too
			counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 45*round(dpifactor/50)) # Change specifically made to fit this plugin
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

		imagedraw.text((dpifactor/50,3*imageresy/5), maintext, font=maintextfont, fill=textcolor)
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
