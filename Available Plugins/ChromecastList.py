#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- ChromecastList.py by @Raminh05
# This is a plugin to fetch Chromecast Devices and display all sorts of info from them!
# What it can do so far: Vertical progress bar, volume bar, vid/track name, app name, device name.

# -- THIS IS A WORK IN PROGRESS! EXPECT A TON OF BUGS. -- #

# -- Bugs so far -- #
# Fetching media title from casting devices is still very borked
# Some graphical glitches with the image generation

# Required deps for ChromecastList.py: Pillow, termcolor, pychromecast

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "ChromecastList"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math

volumecolor = (110,165,237)
playingcolor = (170,110,237)
streamingcolor = (237,122,110)

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

    # -- Import modules -- #
    import pychromecast

    # -- Some functions to handle stuff -- #

    # -- Icon picker for device -- #
    def device_icon_picker(model_name):
        if model_name == 'Chromecast':
            icon_path = GetPathWithinNeighbouringFolder("Chromecast.png", "Chromecast Icons")
        else:
            icon_path = GetPathWithinNeighbouringFolder("gHome.png", "Chromecast Icons")
        return icon_path

    def player_state_icon(player_state):
        if player_state == 'PLAYING' or player_state == 'BUFFERING':
            player_icon_path = GetPathWithinNeighbouringFolder("play_icon.png", "Chromecast Icons")
        elif player_state == 'PAUSED':
            player_icon_path = GetPathWithinNeighbouringFolder("pause_icon.png", "Chromecast Icons")
        else:
            player_icon_path = None
        return player_icon_path
    
    def connect_chromecasts():
        printC("Getting chromecasts...", "blue")
        chromecasts, browser = pychromecast.get_chromecasts(timeout=5)
        for chromecast in chromecasts:
            printC("Connecting to chromecast " + chromecast.device.friendly_name + "....")
            chromecast.connect()
            printC("Waiting chromecast " + chromecast.device.friendly_name + "....")
            chromecast.wait()
        return chromecasts, browser
    
    groupList = []
    chromecasts, browser = connect_chromecasts()
    browser.stop_discovery()
    for chromecast in chromecasts:
        if chromecast.status.status_text == '':
            printC("Idling chromecast detected...Will not display it.", "yellow")
            continue
        else:
            printC("Getting data from chromecast " + chromecast.device.friendly_name + "...", "cyan")
            itemList = []

            friendly_name = chromecast.device.friendly_name
            display_name = chromecast.status.display_name
            media_title = str(chromecast.media_controller.status.title)

            if media_title != None:
                media_title == media_title
            else:
                media_title == "Nothing is playing right now!"

            device_icon = device_icon_picker(chromecast.device.model_name)
            play_icon = player_state_icon(chromecast.media_controller.status.player_state)

            volume_level = chromecast.status.volume_level
            printC("Sucessfully fetched volume level.", "green")

            itemList.append(Item(chromecast.device.friendly_name + " volume", device_icon, volumecolor, bgFillAmt=volume_level))
            printC("Sucessfully finish generating volume item", "green")

            if play_icon != None:
                if chromecast.media_controller.status.duration == None:
                    printC("The media is probably being live-streamed since there's no duration!", "yellow")
                    itemList.append(Item(chromecast.device.friendly_name + " play state", play_icon, streamingcolor, bgFillAmt=1.0))

                else:
                    player_progress = chromecast.media_controller.status.current_time / chromecast.media_controller.status.duration
                    itemList.append(Item(chromecast.device.friendly_name + " play state", play_icon, playingcolor, bgFillAmt=player_progress))
                    printC("Sucessfully gathered player state icon.", "green")

            groupList.append(Group(friendly_name + " | " + display_name + "\n" + media_title, itemList))
            printC("Sucessfully fetched all data from the cast device!", "green")
    
    if groupList:
        maintext = str(len(chromecasts)) + " Chromecasts Detected"
        alttext = maintext + ". " + groupList[0].groupName
    else:
        return None, None, None

    # YOUR CODE HERE! Good luck, soldier.

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
        tilesX = 4
        tilesY = math.floor(len(groupList)/2)+1
        printC("There are " + str(len(groupList)) + " groups in this Card. The card is " + str(tilesY) + " units high.", "yellow")

        # Stuff
        dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
        imageresx = tilesX*dpifactor
        imageresy = tilesY*dpifactor
        image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
        imagedraw = ImageDraw.Draw(image)
        backgroundcolor = (74, 92, 149) # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
        maintextcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
        maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 15*round(dpifactor/50))


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
