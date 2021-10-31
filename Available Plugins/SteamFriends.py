#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- SteamFriends.py
# This plugin uses the Steam Web API to show you what your Steam friends are currently up to.

# Required deps: Pillow, termcolor, steam, requests, wget

# Setup: Get your Steam ID (17 digit number) by heading to your Steam Account Details page. Paste it into the variable below!

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "Steam Friends"
steamID = "" # PASTE YOUR STEAMID HERE
steamKEY = "7867E9A78A0368B729835478837F5293" # Feel free to change at https://steamcommunity.com/dev/apikey

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math
from requests.api import request
from steam import webapi
import requests
import copy
import wget

SMARTFRAMEFOLDER = ""
COLORS = []
width = 2

### YOUR CODE HERE ###
def GetCardData():
	def GetPathWithinNeighbouringFolder(fileWithin, folder):
		file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
		index = file.rfind("/")
		file = file[:index]
		fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
		return fullImagePath
	
	groupList = []
	# Example code:
	#groupList = [Group("O Canada!", [Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5)]),
	#            Group("Our home and\nnative land!", [Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5)]),
	#            Group("True patriot love\nin all of us command", [Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=1), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5)]),
	#            Group("With glowing hearts\nwe see thee rise", [Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5)]),
	#            Group("The True North\nstrong and free!", [Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,255,255), bgFillAmt=0.5), Item("item", "C:\\Users\\mycoo\\OneDrive\\Pictures\\deathstar.png", (255,0,0), bgFillAmt=0.5)])]
	maintext = ""
	alttext = ""
	
	printC("Connecting to the Steam API...", "blue")
	try:
		SteamAPI = webapi.WebAPI(steamKEY)
	except:
		import traceback
		logError("Unable to connect to the Steam API! Check the traceback.", traceback.format_exc(), sourcename)
		return None, None, None

	printC("Getting friends list...", "blue")
	try:
		friendsList = SteamAPI.call('ISteamUser.GetFriendList', steamid=steamID)['friendslist']['friends']
	except:
		import traceback
		logError("Unable to connect to the Steam API! Check the traceback.", traceback.format_exc(), sourcename)
		return None, None, None
	friendCount = str(len(friendsList))
	printC("You have " + str(len(friendsList)) + " friends.", "green")


	printC("Getting more detailed info...", "blue")
	friendsListById = ""
	for friend in friendsList:
		friendsListById += friend['steamid'] + ","
	friendsListById+=steamID

	printC("> Getting friend status...", "blue")
	try:
		friendsList = SteamAPI.call('ISteamUser.GetPlayerSummaries', steamids=friendsListById)['response']['players']
	except:
		import traceback
		logError("Unable to connect to the Steam API! Check the traceback.", traceback.format_exc(), sourcename)
		return None, None, None

	# Assemble online friends
	onlineFriendsList = []
	for friend in friendsList:
		if friend['personastate'] == 1:
			onlineFriendsList.append(friend)

	# Count online friends
	isUserOnline = False
	for friend in onlineFriendsList:
		if friend['steamid'] == steamID:
			isUserOnline = True
			break
	onlineFriendCount = len(onlineFriendsList)
	if isUserOnline:
		printC("You are online!", "cyan")
		onlineFriendCount-=1
	printC(str(onlineFriendCount) + " of your friends are online out of " + str(friendCount) + ".", "green")
	maintext = str(onlineFriendCount) + "/" + str(friendCount) + " online"
	alttext = maintext

	# Continue?
	if len(onlineFriendsList) == 0:
		printC("No one is online! Halting plugin...", "red")
		return None, None, None

	printC("> Getting list of active games...", "blue")
	gameList = []
	# Assemble current games
	for friend in onlineFriendsList:
		if 'gameid' in friend:
			gameList.append(friend['gameid'])

	# Get info for games
	printC("> Getting rich info for games...", "blue")
	gameidList = copy.copy(gameList)
	for game in enumerate(gameList):
		# Get game info
		try:
			StoreRequest = requests.get("https://store.steampowered.com/api/appdetails?appids=" + game[1])
		except:
			printC("Failed to get game data for gameid " + game[1], "red")

		StoreRequest = StoreRequest.json()
		gameList[game[0]] = [game[1], StoreRequest[game[1]]['data']['name'], StoreRequest[game[1]]['data']['header_image']]


	printC("> All info collected! Organizing data...", "blue")
	for friend in onlineFriendsList:
		friendname = friend['personaname']
		friendiconlink = friend['avatarmedium']
		friendplaying = True
		try:
			friendgameid = friend['gameid']
			friendgamestate = friend['gameextrainfo']
		except:
			friendplaying = False
		
		if friendplaying:
			gameindex = gameidList.index(friendgameid)
			gamename = gameList[gameindex][1]
			gamephotolink = gameList[gameindex][2]
			printC("A friend is playing a game! Setting Card width to 4 units.")
			global width
			width = 4

		itemList = [Item("Profile Photo",wget.download(friendiconlink,SMARTFRAMEFOLDER+"/Plugins"),(0,0,0),0)]
		if friendplaying:
			if friendgamestate == gamename:
				groupname = friendname + "\nPlaying " + gamename
			else:
				groupname = friendname + " Playing " + gamename + "\n" + friendgamestate
			itemList.append(Item("Game photo",wget.download(gamephotolink,SMARTFRAMEFOLDER+"/Plugins"),(0,0,0),0))
		else:
			groupname = friendname + "\nIdle"
		
		groupList.append(Group(groupname,itemList))
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
		tilesX = width
		tilesY = math.floor(len(groupList)/2)+1
		printC("There are " + str(len(groupList)) + " groups in this Card. The card is " + str(tilesY) + " units high.", "yellow")
		
		# Stuff
		dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
		imageresx = tilesX*dpifactor
		imageresy = tilesY*dpifactor
		image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
		imagedraw = ImageDraw.Draw(image)
		backgroundcolor = (32,34,40) # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
		maintextcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
		if width == 4:
			maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
		else:
			maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 10*round(dpifactor/50))
	
		
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
		
		# Overlay the icon
		icon = Image.open(self.iconLocation)

		widthratio = icon.size[0]/icon.size[1]
		imsize = (round(xyres*widthratio), round(xyres))
		# Create the image of provided size
		image = Image.new(mode="RGBA", size = imsize)
		imagedraw = ImageDraw.Draw(image)
		icon = icon.resize(imsize)
		try:
			image.paste(icon, (0,0), mask=icon)
		except ValueError:
			image.paste(icon, (0,0))

		os.remove(self.iconLocation)

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
		imagedraw.rectangle([(0,0),xyres], fill=(67,73,83))

		# Overlay Items
		if width == 4:
			padding = round(((2*xyres[0]/3)/6)/20)
			imageWidth = round(((2*xyres[0]/3)/6)-(padding*2))
		else:
			padding = round(((4*xyres[0]/3)/6)/20)
			imageWidth = round(((4*xyres[0]/3)/6)-(padding*2))
		leftmost = padding
		for item in self.itemArray:
			icon = Image.open(item.iconLocation)
			widthratio = icon.size[0]/icon.size[1]
			imsizex = imageWidth*widthratio
			icon.close()

			try:
				itemImage = item.Image(imageWidth, cornerrad)
			except:
				import traceback
				logError("Unknown error with image " + image.imageName + "! Moving on to next image...", traceback.format_exc(), sourcename)
				continue
			image.paste(itemImage, (leftmost, padding*2), mask=itemImage)
			leftmost += round(imsizex)+padding
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
