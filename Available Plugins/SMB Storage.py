#!/usr/bin/python3
# RaddedMC's SMB Storage plugin for SmartFrame
# Built using the SingleRadialProgress template

# This plugin will display the storage capacity of a Linux server on your network.
# It runs the command df | grep 'srvrPath' and 
# To display the storage for multiple servers/shares, just duplicate this file in your plugins folder and put the appropriate info into the duplicate!

# Required deps: Pillow, termcolor, paramiko

srvrPath = ""
sshUsername = ""
sshPWD = ""
sshIP = "192.168.1.133"
sourcename = "SMB Share "

# This plugin uses df to find the storage capacity of a mounted volume.

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import paramiko

SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GetCardData():
	progress = 0.02
	maintext = srvrPath
	alttext = str(round(progress*100))+"% storage used on network server " + maintext
	
	global sourcename
	try:
		sourcename += srvrPath[:srvrPath.index('/')]
	except ValueError:
		try:
			sourcename += srvrPath[:srvrPath.index('\\')]
		except ValueError:
			sourcename += srvrPath
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	printC("Connecting to "+sshIP+"! ", "blue")
	try:
		ssh.connect(sshIP, username=sshUsername, password=sshPWD)
	except:
		import traceback
		logError("Error connecting to server! Check the traceback.", traceback.format_exc(), sourcename)
		return None, None, None
	
	command = "df " + srvrPath + " | tail -1 | awk {'print substr($5, 1, length($5)-1)'}"
	printC("Executing " + command, "blue")
	try:
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
		ssh_stdout = ssh_stdout.read()
		ssh_stderr = ssh_stderr.read()
	except:
		import traceback
		logError("Error executing command! Check the traceback.", traceback.format_exc(), sourcename)
		return None, None, None
	
	try:
		progress = float(ssh_stdout)*0.01
	except:
		import traceback
		logError("Output invalid! Got " + str(ssh_stdout) + " and " + str(ssh_stderr), traceback.format_exc(), sourcename)
		return None, None, None
	
	return progress, maintext, alttext
#### YOUR CODE HERE ####

def GenerateCard():
	# EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
	tilesX = 2 # I don't recommend changing these values for this template
	tilesY = 2 # I don't recommend changing these values for this template
	dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
	backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
	textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
	progressfillcolor = (COLORS[3][0]+50, COLORS[3][1]+50, COLORS[3][2]+50) # Change this to a 3-value tuple to change the color of your progress meter!
	printC("Progress bar fill color is " + str(progressfillcolor))
	progressbgcolor = (COLORS[3][0]-50, COLORS[3][1]-50, COLORS[3][2]-50) # Change this to a 3-value tuple to change the background color of your progress meter!
	printC("Progress bar background color is " + str(progressbgcolor))
	
	imageresx = tilesX*dpifactor
	imageresy = tilesY*dpifactor
	image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
	imagedraw = ImageDraw.Draw(image)                 
	imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)
	
	progress, maintext, alttext = GetCardData()
	
	if maintext and alttext:
		maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))
		if progress < 0.1:
			progresstextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 30*round(dpifactor/50))
			progresstexttop = (imageresy/4)-(dpifactor/10)
		else:
			progresstextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 20*round(dpifactor/50))
			progresstexttop = 5*imageresy/16
		imagedraw.text((dpifactor/50,3*imageresy/4), maintext, font=maintextfont, fill=textcolor)
		circlepos = [(imageresx/8,(imageresy/8)-(dpifactor/10)),(7*imageresx/8, (7*imageresy/8)-(dpifactor/10))]
		imagedraw.arc(circlepos, start=135, end=45, fill=progressbgcolor, width=round(dpifactor/4)) # Background
		imagedraw.arc(circlepos, start=135, end=(270*progress)+135, fill=progressfillcolor, width=round(dpifactor/4)) # Background
		imagedraw.text(((imageresx/4)+(dpifactor/10), progresstexttop), str(round(progress*100))+"%", font=progresstextfont, fill=textcolor)
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
	