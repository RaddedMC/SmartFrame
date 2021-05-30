#!/bin/python3
# RaddedMC's Philips Hue plugin for SmartFrame -- Philips Hue.py
# This plugin gets the state of your Philips Hue smart lights.

# SETUP: Pair your SmartFrame device to your Bridge by pressing the 'link' button on the bridge BEFORE running SmartFrame.
# Paste the IP address of your Philips Hue bridge into the hupipaddr variable.

# Required deps: Pillow, termcolor, phue

sourcename = "Philips Hue"
hueipaddr = "192.168.1.150"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math

SMARTFRAMEFOLDER = ""
COLORS = []

### YOUR CODE HERE ###
def GetCardData():
    def GetPathWithinNeighbouringFolder(fileWithin, folder):
        file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
        index = file.rfind("/")
        file = file[:index]
        fullImagePath = file + "/" + folder + "/" + fileWithin # File location of image
        print(fullImagePath)
        return fullImagePath
    
    groupList = []
    
    # Each Item is a light.
    # Icon is GetPathWithinNeighbouringFolder("light.png", "Philips Hue")
    # bgColor is color of light * brightness
    # bgFillAmt is brightness
    
    # Import Bridge and connect
    from phue import Bridge
    try:
        b = Bridge("192.168.1.150")
        b.connect()
    except:
        printC("Error with Philips Hue! Have you paired your bridge?", "red")
        import traceback
        traceback.print_exc()
        return None, None, None
        
    # For every group...
    for group in b.groups:
        if group.name.startswith("hgrp"): # Some Hue plugin services will add random groups of lights that start with hgrp-###, I don't want these displayed lel
            continue
        lightlist = []
        # For every light that's on
        for light in group.lights:
            if light.on:
                try:
                    hue = light.hue
                    saturation = light.saturation
                    import colorsys
                    color = colorsys.rgb_to_hsv(hue/360, saturation/255, light.brightness/255) # This code is untested. Please let me know if your RGB Hue lights look different.
                except:
                    printC("This light is not RGB. Defaulting to white color")
                    color = (255*(light.brightness/255), 245*(light.brightness/255), 220*(light.brightness/255))
                lightlist.append(Item(light.name, GetPathWithinNeighbouringFolder("light.png", "Philips Hue"), color, light.brightness/255))
        
        if not lightlist:
            printC("There are no lights on in group " + group.name + ". Skipping...")
        else:
            printedname = group.name
            if not group.name.lower().endswith("lights") and not group.name.lower().endswith("light") and not group.name.lower().endswith("lamp") and not group.name.lower().endswith("strip"):
                printedname += " Lights"
            groupList.append(Group(printedname, lightlist))
    
    # Do not add an Item if the light is off
    
    # Each Group is a room.
    # The group's name is the room
    
    numberOfLights = 0
    for group in groupList:
        for item in group.itemArray:
            numberOfLights += 1
    
    maintext = "Philips Hue"
    alttext = "Philips Hue: There are " + str(numberOfLights) + " lights on."
    
    # YOUR CODE HERE! Good luck, soldier.
    
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
        backgroundcolor = (181, 163, 73) # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
        maintextcolor = COLORS[0] # Change this to a 3-value tuple to change the text colour!
        maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 20*round(dpifactor/50))
    
        
        imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)
        padding = dpifactor/50
        top = padding
        for group in groupList:
            printC("Getting Image for group " + group.groupName)
            try:
                groupImg = group.Image((round(imageresx-(padding*2)),round(11*dpifactor/24)), dpifactor/10)
            except:
                printC("Unknown error with group " + group.groupName + "! Moving on to next group...", "red")
                import traceback
                traceback.print_exc()
                continue
            image.paste(groupImg, (round(padding), round(top)), mask = groupImg)
            top += (11*dpifactor/24) + padding
        imagedraw.text((padding, top), maintext, fill=maintextcolor, font=maintextfont)
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
        imagedraw.rounded_rectangle([(0,round(xyres*(1-self.bgFillAmt))),(xyres,xyres)], fill=(round(self.bgColor[0]), round(self.bgColor[0]), round(self.bgColor[0])), radius=round(cornerrad)) # FG
        
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
                printC("Unknown error with image " + group.imageName + "! Moving on to next image...", "red")
                import traceback
                traceback.print_exc()
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