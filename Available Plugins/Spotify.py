#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- Spotify.py
# This plugin grabs information about a song that's currently playing on your Spotify account.

# Required deps: Pillow, termcolor, colorgram.py, spotipy, wget

# IMPORTANT SETUP:
# Spotify's API requires user authentication. Please fill the following variables:
# spotifyUsername = your account username
# spotifyClientID / spotifyClientSecret -- You need to make an application in Spotify's developer console. https://developer.spotify.com/dashboard
# redirect_uri -- If you know what you're doing (let me know how to make this better! open an issue on github!), go ahead and change this.
#                 Otherwise, copy the value within the "quotes" to your application in the Spotify dashboard.

# Make sure you run SmartFrame in the FOREGROUND when you run this plugin for the first time.
# This application will open a web browser where you need to log into your Spotify account.
# IF YOU ARE RUNNING HEADLESS: you need to pipe an X session to your local machine with a web browser.
			#I know this is a stupid solution, so if you know how to improve this, PLEASE LET ME KNOW (create an issue on Github or join https://discord.gg/9Ms4bFw)!

sourcename = "Spotify"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import colorgram
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SMARTFRAMEFOLDER = ""
COLORS = []

spotifyUsername = ""
spotifyClientID = "" # Get yours at https://developer.spotify.com/dashboard
spotifyClientSecret = ""
redirect_uri = "http://127.0.0.1:9090" # Set this to your URI in the Spotify dashboard


### YOUR CODE HERE ###
def GetCardData():

	def GetPathWithinNeighbouringFolder(fileWithin, folder):
		file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
		index = file.rfind("/")
		file = file[:index]
		fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
		return fullImagePath

	progress = 0.1 # Float between 0 and 1
	songname = ""
	artistname = ""
	albumArtLocation = GetPathWithinNeighbouringFolder("", "")
	othertext = "Your App Name\nStatus"
	alttext = "Whatever you want!"
	
	# Authenticate and get data
	try:
		scope = "user-read-playback-state"
		oauth = SpotifyOAuth(scope=scope, redirect_uri=redirect_uri, cache_path=__file__+".spotifcache", client_id=spotifyClientID, client_secret=spotifyClientSecret)
		spotify = spotipy.Spotify(auth_manager=oauth)
		printC("Connecting to Spotify...", "blue")
		current_track = spotify.current_playback(additional_types="episode")
	except:
		import traceback
		logError("Error getting Spotify data! Returning null card...", traceback.format_exc(), sourcename)
		return None, None, None, None, None, None
		
		
	# Parse data
	if not current_track or not current_track['is_playing']:
		# Not playing
		printC("Spotify is not playing anything.", "yellow")
		return None, None, None, None, None, None
	else:
		url = ""
	
		# Name
		songname = current_track['item']['name']
		
		# Progress
		progress = current_track['progress_ms']/current_track['item']['duration_ms']
		
		# Device name
		devicename = ""
		for device in spotify.devices()['devices']:
			if device['is_active']:
				devicename = device['name']
				
		othertext = "Spotify | On " + devicename
	
		if current_track['item']['type'] == "episode":   # Podcast
			printC("Podcast!")
			artistname = current_track['item']['show']['name']
			url = current_track['item']['show']['images'][1]['url']
			
		else:   # Song
			# Artist name
			for artist in current_track['item']['artists'][:-1]:
				artistname += artist['name'] + ", "
			artistname += current_track['item']['artists'][-1]['name']
					
			# Playlist name
			try:
				current_list = spotify.user_playlist(user="RaddedMC", playlist_id=current_track["context"]["uri"], fields="name")['name']
				printC("Playlist!")
			except:
				current_list = ""
				# No specific playlist
			
			othertext += "\n" + current_list
			
			url = current_track['item']['album']['images'][1]['url']
			
		import wget
		try:
			albumArtLocation = wget.download(url,__file__+".image.jpg")
			printC("Downloaded album art! Saved to " + albumArtLocation, "green")
		except:
			printC("Failed to download album art!", "red")
			import traceback
			traceback.print_exc()
				
	alttext = "Spotify is playing " + songname + " by " + artistname
	return progress, songname, artistname, albumArtLocation, othertext, alttext
### YOUR CODE HERE ###



def GenerateCard():
	tilesX = 2 # Change this to change tile size
	tilesY = 2 # Change this to change tile size
	dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
	backgroundOverrideColor = COLORS[3] # This color will be displayed in the background if album art can't be found or displayed.
	songtextcolor = COLORS[0]
	artisttextcolor = COLORS[1]
	songtextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 12*round(dpifactor/50))
	artisttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 10*round(dpifactor/50))
	othertextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 7*round(dpifactor/50))
	
	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGBA", (tilesX*dpifactor, tilesY*dpifactor))
	
	padding = round(dpifactor/25)
	
	progress, songname, artistname, albumArtLocation, othertext, alttext = GetCardData()
	
	if songname:
		
		deleteimage = True
		
		try:
			printC("Running colorgram...", "blue")
			albumartcolour = colorgram.extract(albumArtLocation, 1)[0].rgb
			printC("Colorgram done!", "green")
			
			# Tune colours
			import colorsys
			albumartcolourhsv = colorsys.rgb_to_hsv(albumartcolour[0]/255, albumartcolour[1]/255, albumartcolour[2]/255)
			if albumartcolourhsv[2] > 0.9:
				printC("Superbright!!")
				albumartcolour = (albumartcolour[0]-200, albumartcolour[1]-200, albumartcolour[2]-200)
				progressbarcolor = (albumartcolour[0]+150, albumartcolour[1]+150, albumartcolour[2]+150)
				transparency = 220
			elif albumartcolourhsv[2] > 0.6:
				printC("Bright!!")
				albumartcolour = (albumartcolour[0]-100, albumartcolour[1]-100, albumartcolour[2]-100)
				progressbarcolor = (albumartcolour[0]+150, albumartcolour[1]+150, albumartcolour[2]+150)
				transparency = 180
			elif albumartcolourhsv[2] < 0.2:
				printC("Dark!!")
				albumartcolour = (albumartcolour[0], albumartcolour[1], albumartcolour[2])
				progressbarcolor = (albumartcolour[0]+175, albumartcolour[1]+175, albumartcolour[2]+175)
				transparency = 150
			else:
				printC("Normal!!")
				progressbarcolor = (albumartcolour[0]+100, albumartcolour[1]+100, albumartcolour[2]+100)
				transparency = 100
			
			# Get album art
			albumart = Image.open(albumArtLocation)
			albumart = albumart.resize((imageresx, imageresy))
			image.paste(albumart, (0, 0))
			
			# Background darken overlay thing
			overlay = Image.new("RGBA", (imageresx, imageresy))
			overlayDraw = ImageDraw.Draw(overlay)
			overlayDraw.rectangle([(0,0), (imageresx, imageresy)], fill=(albumartcolour[0], albumartcolour[1], albumartcolour[2], transparency)) # Semitransparent overlay for text contrast
			image = Image.alpha_composite(image, overlay)
			
		except:
			imagedraw = ImageDraw.Draw(image)  
			imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundOverrideColor) # Background if it can't get an image
			progressbarcolor = (backgroundOverrideColor[0]+50, backgroundOverrideColor[1]+50, backgroundOverrideColor[2]+50)
			import traceback
			logError("Unable to display album art or set progress bar color! Check out the traceback!", traceback.format_exc(), sourcename)
			deleteimage = False
		
		imagedraw = ImageDraw.Draw(image)  
			
		if deleteimage:
			try:
				printC("Deleting album art image " + albumArtLocation)
				os.remove(albumArtLocation)
			except:
				import traceback
				logError("Unable to delete album art image! Check out the traceback!", traceback.format_exc(), sourcename)
			
			
		imagedraw.text((padding, padding*2), songname, font=songtextfont, fill=songtextcolor) # Song name
		imagedraw.text((padding, (padding*2)+round(dpifactor/4)), artistname, font=artisttextfont, fill=artisttextcolor) # Artist name
		imagedraw.text((padding, imageresy-round(5*dpifactor/12)), othertext, font=othertextfont, fill=artisttextcolor) # App name
		overlay = Image.new("RGBA", (imageresx, imageresy))
		overlayDraw = ImageDraw.Draw(overlay)
		overlayDraw.rounded_rectangle([(padding, round(2*imageresy/3)), (imageresx-padding, round(2*imageresy/3)+round(4*padding))], fill=(255,255,255,50), radius=round(dpifactor/5)) # Progress meter BG
		image = Image.alpha_composite(image, overlay)
		imagedraw = ImageDraw.Draw(image)
		if progress >= 0.1:
			imagedraw.rounded_rectangle([(padding, round(2*imageresy/3)), (progress*(imageresx-padding), round(2*imageresy/3)+round(4*padding))], fill=progressbarcolor, radius=round(dpifactor/5)) # Progress meter FG
		
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
	
