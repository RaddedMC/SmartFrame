#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- MediaPlayer.py
# This is a plugin template for SmartFrame v2.
# This particular template is meant for media
#it can display an album art and generates a nicely formatted Card with progress, song and artist names,
#and other information.

# Required deps: Pillow, termcolor, colorgram.py

# DEVELOPER INSTRUCTIONS:
# Assume you have root priveleges.
# Use the variables in GetCardData() to change the tile size and pixel density of your Card.
# If you need additional files, place them into a folder of the same name as your plugin.
# Use GetPathWithinNeighbouringFolder to get the files from this folder.
# Make sure that the image isn't too large! A large image can take a long time for weaker computers to process colors from.

# Make sure to change the following variables:
# sourcename, progress, songname, artistname, albumArtLocation, othertext, alttext.

# For debug/overflow purposes, make sure you set alttext to something that accurately represents your collected data.
# Use printC(text, color of text) if you need to print. 

# To test, just run your card in a terminal! The image will appear in your Smartframe/Cards folder. I recommend deleting this file before running SmartFrame again.
# Note that if your plugin crashes, it will not take down the whole SmartFrame process. However, tracebacks will be outputted to the user.

# When you're ready to release to the main repo, place all your code and related files in a folder and place it into Available Plugins/, then make a pull request!

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "Set your card's default sourcename here"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import colorgram

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

    progress = 0.1 # Float between 0 and 1
    songname = "Megalovania"
    artistname = "Toby Fox"
    albumArtLocation = GetPathWithinNeighbouringFolder("", "")
    othertext = "Your App Name\nStatus"
    alttext = "Whatever you want!"
    
    # Your code here
    
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
        
        try:
            printC("Running colorgram...", "blue")
            albumartcolour = colorgram.extract(albumArtLocation, 1)[0].rgb
            progressbarcolor = (albumartcolour[0]+75, albumartcolour[1]+75, albumartcolour[2]+75)
            printC("Colorgram done!", "green")
            
            # Get album art
            albumart = Image.open(albumArtLocation)
            albumart = albumart.resize((imageresx, imageresy))
            image.paste(albumart, (0, 0))
            
            # Background darken overlay thing
            overlay = Image.new("RGBA", (imageresx, imageresy))
            overlayDraw = ImageDraw.Draw(overlay)
            overlayDraw.rectangle([(0,0), (imageresx, imageresy)], fill=(albumartcolour[0]-100,albumartcolour[1]-100,albumartcolour[2]-100,200)) # Semitransparent overlay for text contrast
            image = Image.alpha_composite(image, overlay)
            
        except:
            imagedraw = ImageDraw.Draw(image)  
            imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundOverrideColor) # Background if it can't get an image
            printC("Unable to display album art or set progress bar color! Check out the traceback!", "red")
            progressbarcolor = (backgroundOverrideColor[0]+50, backgroundOverrideColor[1]+50, backgroundOverrideColor[2]+50)
            import traceback
            traceback.print_exc()
        
        imagedraw = ImageDraw.Draw(image)  
            
        imagedraw.text((padding, padding*2), songname, font=songtextfont, fill=songtextcolor) # Song name
        imagedraw.text((padding, (padding*2)+round(dpifactor/4)), artistname, font=artisttextfont, fill=artisttextcolor) # Artist name
        imagedraw.text((padding, imageresy-round(5*dpifactor/12)), othertext, font=othertextfont, fill=artisttextcolor) # App name
        imagedraw.rounded_rectangle([(padding, round(2*imageresy/3)), (imageresx-padding, round(2*imageresy/3)+round(4*padding))], fill=(255,255,255,50), radius=round(dpifactor/5)) # Progress meter BG
        if progress >= 0.1:
            imagedraw.rounded_rectangle([(padding, round(2*imageresy/3)), (progress*(imageresx-padding), round(2*imageresy/3)+round(4*padding))], fill=progressbarcolor, radius=round(dpifactor/5)) # Progress meter FG
        
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
    