#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- OutlookCalendar.py
# This plugin grabs your day's events from an Outlook Calendar

# SETUP:
#    See https://pypi.org/project/O365/#authentication for instructions on getting an Api ID and Secret if my keys don't work
#    Change the calendarName variable to select the subcalendar you wish the plugin to show
#    Get an OAuth token:
#        On first run, you will be given a link to log into your Microsoft account. Here you will see the permissions on your account that the plugin requests.
#        Once logged in, your browser will take you to a blank screen. Copy/paste the URL of this blank site into your terminal.
#        You are now logged in! You won't need to do this again.
#		 By default, the plugin will grab events occuring up to 4 hours from when it is ran. To increase this range, adjust the timeerangehrs variable.
#    To log out, delete SmartFrame/o365_token.txt


# Required deps: Pillow, termcolor, O365, wget

# Add any user-definable variables here! (API keys, usernames, etc.)
apiID = "" # See instructions to get an ID and secret at https://pypi.org/project/O365/#authentication
apiSecret = ""
calendarName = "Calendar" # Most Outlook accounts have their default calendar just named Calendar
timerangehrs = 4 # Adjust to get a larger range of events, default is 4
googlemapsapikey = "" # Add an API key to get location backgrounds and other pretties based on your vevent locations :D
# TODO: remove this and go based on events in a day

sourcename = "Outlook Calendar " + calendarName

# imports
from PIL import Image, ImageFont, ImageDraw
import os, math
import sys
import datetime
from O365 import Account
import wget # For map backgrounds


SMARTFRAMEFOLDER = ""
COLORS = []

def CalendarMain():

	# init variables
	events = []
	account = Account((apiID, apiSecret))

	# Try to login and grab calendar
	try:
		printC("Logging in...", "blue")
		calendar = account.schedule().get_calendar(calendar_name=calendarName)
	except RuntimeError:
		# If it doesn't work, authenticate!
		printC("Starting authentication! If this is the first time you've ran this plugin, please see the instructions at the top of Plugins/OutlookCalendar.py or follow the instructions below:", "yellow")
		try:
			account.authenticate(scopes = ['basic', 'calendar', 'calendar_shared'])
		except:
			import traceback
			logError("Error while authenticating! See the traceback for more details.", traceback.format_exc(), sourcename)
			return None
	printC("Logged into Office account!", "green")

	# Grab events from specified range
	today = datetime.datetime.now()
	endrange = today + datetime.timedelta(hours = timerangehrs)

	printC("Querying events from " + today.__str__() + " to " + endrange.__str__())
	query = calendar.new_query('start').greater_equal(today)
	query.chain('and').on_attribute('end').less_equal(endrange)
	calendarEvents = calendar.get_events(query = query, include_recurring=True)
 
	# Create Event objects for each event
	if calendarEvents:
		for calendarEvent in calendarEvents:
			# Pick a colour!
			colour = COLORS[3]
			category = calendarEvent.categories
			if calendarEvent.is_cancelled:
				colour = (100, 100, 100)
			elif "Red category" in category:
				colour = (135, 34, 34)
			elif "Orange category" in category:
				colour = (135, 78, 34)
			elif "Yellow category" in category:
				colour = (106, 110, 27)
			elif "Green category" in category:
				colour = (66, 135, 34)
			elif "Blue category" in category:
				colour = (34, 86, 135)
			elif "Purple category" in category:
				colour = (91, 34, 135)

			# Grab map photo if needed
			if googlemapsapikey and calendarEvent.location['displayName'] != '':
				import colorsys
				mapcolour = colorsys.hls_to_rgb(colorsys.rgb_to_hls(colour[0]/255, colour[1]/255, colour[2]/255)[0],0.72,0.50)

				# There is a location! Grab the photo!!
				import urllib.parse
				url = "https://maps.googleapis.com/maps/api/staticmap?key=" + urllib.parse.quote(googlemapsapikey)\
					+ "&center=" + urllib.parse.quote(calendarEvent.location['displayName'])\
					+ "&zoom=18" + "&format=png"\
					+ "&maptype=roadmap"\
					+ "&style=element:geometry%7Ccolor:0x0f1114&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0xededed&style=element:labels.text.stroke%7Ccolor:0x18191b&style=feature:administrative%7Celement:geometry%7Ccolor:0x757575&style=feature:administrative%7Celement:geometry.fill%7Ccolor:0x262626&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0x707070&style=feature:administrative%7Celement:labels.text.stroke%7Ccolor:0x1a1a1a&style=feature:administrative.country%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.locality%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:landscape.man_made%7Ccolor:0x000000&style=feature:landscape.natural%7Ccolor:0x001906&style=feature:landscape.natural.terrain%7Celement:geometry%7Ccolor:0x333833&style=feature:poi%7Celement:labels%7Cvisibility:off&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Celement:geometry%7Ccolor:0x101e1e&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:poi.park%7Celement:labels.text.stroke%7Ccolor:0x1b1b1b&style=feature:road%7Celement:geometry.fill%7Ccolor:0x"\
					+ urllib.parse.quote(('%02x%02x%02x' % (round(mapcolour[0]*255), round(mapcolour[1]*255), round(mapcolour[2]*255))))\
					+ "&style=feature:road%7Celement:geometry.stroke%7Ccolor:0x0f1114&style=feature:road%7Celement:labels.text.fill%7Ccolor:0xededed&style=feature:road%7Celement:labels.text.stroke%7Ccolor:0x000000&style=feature:road.highway%7Celement:geometry%7Ccolor:0x51bcd6&style=feature:road.highway%7Celement:geometry.fill%7Ccolor:0x51bcd6&style=feature:road.highway%7Celement:geometry.stroke%7Ccolor:0x0b0b0f&style=feature:road.highway%7Celement:labels.icon%7Cvisibility:off&style=feature:road.highway%7Celement:labels.text.fill%7Ccolor:0xffffff&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0xd1d1d1&style=feature:transit%7Celement:labels.icon%7Cvisibility:off&style=feature:transit%7Celement:labels.text.fill%7Ccolor:0x666666&style=feature:water%7Celement:geometry%7Ccolor:0x011428&style=feature:water%7Celement:labels.text.fill%7Ccolor:0xa3a3a3&size=900x100"

				imagelocation = wget.download(url, __file__ + calendarEvent.subject + "-map.png")
			else:
				imagelocation = None

			events.append(event(calendarEvent.subject, calendarEvent.location['displayName'], calendarEvent.start, calendarEvent.end, colour, calendarEvent.is_all_day, imagelocation if 'imagelocation' in locals() else None))
			
	else:
		printC("No events!", "yellow")
		return None

	# Done! Good job, internet.
	return events

class event:
			 #TODO: icons
			 #TODO: map image background
	eventName = ""
	eventLocationName = ""
	eventStartTime = None
	eventEndTime = None
	eventBgColor = (0,0,0)
	eventMapPhotoFileLocation = None
	eventMapPhoto = None
	IsAllDay = False

	def __init__(self, eventName, eventLocationName, eventStartTime, eventEndTime, eventBgColor, isAllDay, photoFileName):
		self.eventName = eventName
		self.eventLocationName = eventLocationName
		self.eventStartTime = eventStartTime
		self.eventEndTime = eventEndTime
		self.eventBgColor = eventBgColor
		self.IsAllDay = isAllDay

		if photoFileName:
			self.eventMapPhotoFileLocation = photoFileName
			self.eventMapPhoto = Image.open(photoFileName)

		print("New Event | " + self.eventName + self.eventStartTime.strftime(" at %I:%M %p on %m/%d/%Y to ") + self.eventEndTime.strftime("%I:%M %p on %m/%d/%Y"))

	def __str__(self):
		print("Event " + self.eventName + self.eventStartTime.strftime(" at %I:%M %p on %m/%d/%Y to ") + self.eventEndTime.strftime("%I:%M %p on %m/%d/%Y"))

	def Image(self, xyres, cornerrad):
		image = Image.new("RGBA", xyres)

		# Map background
		if self.eventMapPhoto:
			# Image and masking
			self.eventMapPhoto = self.eventMapPhoto.resize(xyres)
			mask = Image.new('L', xyres, 0)
			maskDraw = ImageDraw.Draw(mask)
			maskDraw.rounded_rectangle([[0,0],xyres], fill = 255, radius=cornerrad)
			self.eventMapPhoto.putalpha(mask)
			image.paste(self.eventMapPhoto, (0,0))

			# Background
			overlay = Image.new("RGBA", xyres)
			overlayDraw = ImageDraw.Draw(overlay)
			overlayDraw.rounded_rectangle([[0,0],xyres], fill=(self.eventBgColor[0],self.eventBgColor[1],self.eventBgColor[2],200), radius=cornerrad)
			image = Image.alpha_composite(image, overlay)
		
		imagedraw = ImageDraw.Draw(image)
		
		if not self.eventMapPhoto:
			imagedraw.rounded_rectangle([[0,0],xyres], fill=self.eventBgColor, radius=cornerrad)

	
		
		# Icon for event
		# TODO: make this an actual icon
		imagedraw.ellipse([xyres[0]/80, xyres[0]/80, 10*xyres[1]/11, 10*xyres[1]/11], fill=(round(self.eventBgColor[0]*1.6),round(self.eventBgColor[1]*1.6),round(self.eventBgColor[2]*1.6)))

		# Event text
		maintextcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", round(40*xyres[1]/111))

		eventtext = self.eventName + "\n"
		 # time
		if self.IsAllDay:
			eventtext += "All day!"
		else:
			eventtext += self.eventStartTime.strftime("%I:%M %p - ") + self.eventEndTime.strftime("%I:%M %p")
		 # location
		if self.eventLocationName:
			eventtext += " at " + self.eventLocationName

		imagedraw.text([xyres[0]/60+10*xyres[1]/11, xyres[1]/32], eventtext, fill=maintextcolor, font=maintextfont)

		# Delete photos!
		if self.eventMapPhoto:
			try:
				os.remove(self.eventMapPhotoFileLocation)
			except PermissionError:
				pass
			except:
				import traceback
				logError("Unknown error attempting to delete image " + self.eventMapPhotoFileLocation + "! Moving on...", traceback.format_exc(), sourcename)

		return image

#### YOUR CODE HERE ####
def GenerateCard():

	# Your code here
	events = CalendarMain()
	if (events):
		# -- Gather photo meta --
		alttext = "Outlook Calendar: " + calendarName + " - " + str(len(events)) + " events"
		tilesYScalable = math.ceil(len(events)/2)
		tilesY = tilesYScalable if tilesYScalable < 4 else 4

		tilesX = 4 # Change this to change tile size
		dpifactor = 600 # Change this to increase card resolution. Don't go too high!!!
		padding = dpifactor/10
		imageresx = tilesX*dpifactor
		imageresy = tilesY*dpifactor
		image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
		imagedraw = ImageDraw.Draw(image)                 

		if len(events) != 1:
			top = padding/2
		else:
			top = round(padding * 3)

		# -- CREATE IMAGE -- #
		#TODO: include date? (tomorrow, wednesday, etc.)
		for eventData in events:
			printC("Getting image for event " + eventData.eventName)
			try:
				eventImg = eventData.Image((round(imageresx-(padding*1.5)),round(10*dpifactor/24)), dpifactor/2)
			except:
				import traceback
				logError("Unknown error with event " + eventData.eventName + "! Moving on to next group...", traceback.format_exc(), sourcename)
				continue
			image.paste(eventImg, (round(padding/2), round(top)), mask = eventImg)
			top += (11*dpifactor/24) + padding/4

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
	