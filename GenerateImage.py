# RaddedMC's SmartFrame v2 -- GenerateImage.py
# This program generates an image that is to be sent to the display source.
# Required deps: PIL, Card
# KEY FILES: Fonts/font1.ttf
#            Colors.txt

def printG(string):
    print("Image Generator | " + str(string))

def GenerateImage(cardsinstance, resx, resy):
    # Imports and key variables
    cards = cardsinstance.copy()
    
    printG("Importing libraries...")
    from PIL import Image, ImageFont, ImageDraw
    from Card import Card
    from time import gmtime, strftime
    import os
    import math
    
    printG("Rendering image:")
    mainimage = Image.new(mode = "RGB", size = (resx, resy))
    maindraw = ImageDraw.Draw(mainimage)
    
    
    # Assets
    printG("Gathering fonts...")
    pixelratio = resx/400
    textsizes = [50*pixelratio, 40*pixelratio, 30*pixelratio, 20*pixelratio]
    fonts = []
    for textsize in textsizes:
        fonts.append(ImageFont.truetype("Fonts/font1.ttf",round(textsize)))
        
    printG("Gathering colors...")
    colorfile = open('Colors.txt', 'r')
    colorfileLines = colorfile.readlines()
    colors = []
    for line in colorfileLines:
        if "#" in line:
            break
        if len(colors) == 5:
            printG("Reached color limit! SmartFrame currently only allows 5 theme colors.")
            break
        else:
            colors.append((int(line[0:3]), int(line[4:7]), int(line[8:11])))
            printG("Added color " + line[0:3] + " " + line[4:7] + " " + line[8:11] + "!")
    
    printG("All assets prepared.")
    
    
    # Draw background
    
    printG("Generated: Background")
    
    
    # Draw time
    # Reserve top 15% for clock
    maxclockheight = round(resy*0.15)
    maindraw.rectangle([(0,0),(resx, maxclockheight)], outline=colors[4],width=round(pixelratio))
    
    maindraw.text((10*pixelratio,0), strftime("%I:%M"), fill=colors[1], font=fonts[0]) #Hour
    maindraw.text((150*pixelratio,10*pixelratio), strftime("%p"), fill=colors[1], font=fonts[1]) #AM/PM
    maindraw.text((10*pixelratio, 55*pixelratio), strftime("%A, %b %d, %Y"), fill=(255,255,255), font=fonts[2]) #Date
    
    printG("Generated: Time")
    
    
    # Draw cards
    cardsx = math.floor(resx/pixelratio/100)
    cardsy = math.floor((resy-maxclockheight)/pixelratio/100)
    printG("This SmartFrame (" + str(resx) + "x" + str(resy)+ ") can fit a " + str(cardsx) + "x" + str(cardsy) + " grid of cards.")
    cardarray = [[False]*cardsy]*cardsx # False = unused, True = used
        
    printG("Calculating spaces...")
    nocards = False
    # Loop through each x and y.
    for x in range(len(cardarray)):
        for y in range(len(cardarray)):
            # If there are no more cards, stop finding places for them
            if len(cards) == 0:
                printG("Out of cards! Generation complete!")
                nocards = True
                break
        
            # If space is filled, move to next space.
            if cardarray[x][y]:
                printG("("+str(x)+", "+str(y)+") is filled!")
                continue
            # If space is not filled:
            else:
                printG("("+str(x)+", "+str(y)+") is empty!")
                currentcard = cards[0] # Grab first card
                currentcardrange = "[ (" + str(x) + ", " + str(y)+"), (" + str(x+currentcard.tilesx) + ", " + str(y+currentcard.tilesy) + ") ]"
                printG("Trying card " + currentcard.sourcename + " with size ("+ str(currentcard.tilesx) + ", " + str(currentcard.tilesy)+ ") in area " + currentcardrange + "...")
                used = False
                for cardx in range(x,x+currentcard.tilesx): # If space+(1-x of card) and space +(1-y of card) are all false,
                    for cardy in range(y,y+currentcard.tilesy):
                        try:
                            if cardarray[cardx][cardy]:
                                # If not, iterate to next space
                                used = True
                        except IndexError:
                            # If not, iterate to next space
                            printG("("+str(cardx)+", "+str(cardy)+") is out of range! Stopping check...")
                            used = True
                        if used:
                            # If not, iterate to next space
                            printG("("+str(cardx)+", "+str(cardy)+") is filled! Stopping check...")
                            break
                        else:
                            printG("("+str(cardx)+", "+str(cardy)+") is empty...")
                    if used:
                        # If not, iterate to next space
                        break
                if used:
                    # If not, iterate to next space
                    continue
                else:
                    printG("All space for card " + currentcard.sourcename + " is empty! Stopping check...")
                    # set target cells to filled
                    printG("Setting range " + currentcardrange + " to filled...")
                    for cardx in range(x, x+currentcard.tilesx):
                        for cardy in range(y, y+currentcard.tilesy):
                            cardarray[x][y] = True
                    
                    # place card!
                    printG("Placing card " + currentcard.sourcename + "...")
                    
                    # pop card from array!
                    printG("Card placed successfully! Removing from array...")
                    cards.pop(0)
        if nocards:
            break
    
    
    # Alt text / overflow
    alttext = ""
    if len(cards) != 0:
        alttext = cards[0].sourcename + ": " + cards[0].alttext
        if len(cards) > 1:
            remainingcards = len(cards)-1
            if remainingcards > 1:
                alttext+=" and " + str(remainingcards) + " more cards"
            else:
                alttext+=" and 1 more card"
        printG("Some cards remaining! Setting alttext to \"" + alttext + "\"")
    
    
    # Done!
    printG("Image generated!")
    return mainimage



# Test code
from PIL import Image, ImageFont, ImageDraw
from Card import Card
from time import gmtime, strftime
import os
import math
files = os.listdir("Cards")

cards = [Card(files[0], "poggers", files[0], 2, 2),
         Card(files[1], "poggers", files[1], 4, 4),
         Card(files[2], "poggers", files[2], 4, 2),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[3], "poggers", files[3], 1, 1),
         Card(files[2], "poggers", files[2], 4, 2),
         Card(files[2], "poggers", files[2], 4, 2),
         Card(files[2], "poggers", files[2], 4, 2),]
    
GenerateImage(cards, 720, 1280).show()
GenerateImage(cards, 1080, 1920).show()
GenerateImage(cards, 2160, 3840).show()