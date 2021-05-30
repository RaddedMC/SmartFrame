#!/bin/python3
# RaddedMC's Wifi Status icon for SmartFrame -- 1WifiStatus.py
# This is a simple icon that gets wifi signal status.

# Make sure you keep the 1WifiStatus folder in the same path as the plugin!
# Required deps: Pillow, termcolor, pywifi, comtypes, access_points

# No setup is required other than installing dependencies.

sourcename = "Wifi Status"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import pywifi
import access_points
from pywifi import const

SMARTFRAMEFOLDER = ""
COLORS = []

interfaceoverride = 0 # If your device is weird and wifi isn't the first interface listed

#### YOUR CODE HERE ####
def GetCardData():
    imagePath = "1WifiStatus Icons" # File within same folder as plugin (I recommend creating a subfolder with assets related to your plugin
    
    background = (50,50,100) # Red, Green, Blue
    alttext = "Whatever you want!"
    
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[interfaceoverride]
    if iface.status() is not const.IFACE_CONNECTED:
        # Wifi is not connected
        printC("No wifi! Either you're using ethernet or are offline.", "red")
        return None, None, None
    else:
        wifiScanner = access_points.get_scanner()
        try:
            wifiStrength = wifiScanner.get_access_points()[0].quality
        except:
            printC("Unknown error! Check the traceback!", "red")
            import traceback
            traceback.print_exc()
            exit()
            
        if wifiStrength >= 0 and wifiStrength <= 25:
            # LOW
            imagePath += "/wifi-low.png"
            alttext = "Wifi Strength is low!"
            printC(alttext)
        elif wifiStrength > 25 and wifiStrength <= 50:
            # MEDIUM
            imagePath += "/wifi-medium.png"
            alttext = "Wifi Strength is medium!"
            printC(alttext)
        elif wifiStrength > 50 and wifiStrength <= 75:
            # HIGH
            imagePath += "/wifi-semifull.png"
            alttext = "Wifi Strength is high!"
            printC(alttext)
        else:
            # HIGHEST
            imagePath += "/wifi-full.png"
            alttext = "Wifi Strength is highest!"
            printC(alttext)
    
    file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
    index = file.rfind("/")
    file = file[:index]
    fullImagePath = file + "/" + imagePath # File location of image
    
    return fullImagePath, background, alttext
#### YOUR CODE HERE ####

def GenerateCard():
    tilesX = 1 # Change this to change tile size
    tilesY = 1 # Change this to change tile size
    dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
    imageresx = tilesX*dpifactor
    imageresy = tilesY*dpifactor
    image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
    imagedraw = ImageDraw.Draw(image)
    
    imageFile, background, alttext = GetCardData()
    
    if image and background and alttext:
        imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=background)
        icon = Image.open(imageFile)
        icon = icon.resize((round(imageresx-(dpifactor/12)), round(imageresy-(dpifactor/12))))
        image.paste(icon, (round(dpifactor/25), round(dpifactor/25)), mask=icon)
    else:
        printC("No data! Sending null data.", "red")
        return None, None, None, None
    
    return image, alttext, tilesX, tilesY



### SmartFrame.py calls this to get a card. I don't recommend editing this.
def GetCard():

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
    from Card import Card
    
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
        
        return Card(outputLocation, alttext, sourcename, tilesX, tilesY)
    else:
        # No cards
        printC("No cards to return!...", "red")
        return None
    
def printC(string, color = "white"):
    from termcolor import colored
    print(sourcename + " | " + colored(str(string), color))
    
if __name__ == "__main__":
    GetCard()
    