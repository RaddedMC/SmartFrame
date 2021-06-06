# RaddedMC's SmartFrame v2 -- GenerateImage.py
# This program generates an image that is to be sent to the display source.

# GenerateImage(cardsinstance, resx, resy, scale)
# cardsinstance -- an array of cards, this will be copied and your original variable will not be changed
# resx & resy   -- X and Y resolution
# scale         -- an integer to adjust the size of everything, larger value = smaller text and more cards

# printG() -- just a simple output formatter

# Required deps: Pillow, Card, termcolor
# KEY FILES: Fonts/font1.ttf
#            Colors.txt

from ErrorLogger import logError

moduleName = "Image Generator"

def printG(string, color = "white"):
	from termcolor import colored
	print("Image Generator | " + colored(str(string), color))

def GenerateImage(cardsinstance, resx, resy, scale):
	try:
		# Imports and key variables
		cards = cardsinstance.copy()
		
		printG("Importing libraries...", "blue")
		from PIL import Image, ImageFont, ImageDraw
		from Card import Card
		from time import gmtime, strftime
		import os
		import math
		
		
		# PRINT COLORS:
		# Blue = doing something -- header
		# Green = done something!
		# Yellow = important part of thing being done
		# Red = error
		
		printG("Rendering image:", "blue")
		mainimage = Image.new(mode = "RGB", size = (resx, resy))
		maindraw = ImageDraw.Draw(mainimage)
		
		
		# Assets
		printG("Gathering fonts...", "blue")
		pixelratio = resx/(scale * 100)
		textsizes = [50*pixelratio, 40*pixelratio, 30*pixelratio, 15*pixelratio]
		fonts = []
		for textsize in textsizes:
			fonts.append(ImageFont.truetype("Fonts/font1.ttf",round(textsize)))
			
		printG("Gathering colors...", "blue")
		colorfile = open('Colors.txt', 'r')
		colorfileLines = colorfile.readlines()
		colors = []
		for line in colorfileLines:
			if "#" in line:
				break
			else:
				colors.append((int(line[0:3]), int(line[4:7]), int(line[8:11])))
				printG("Added color " + line[0:3] + " " + line[4:7] + " " + line[8:11] + "!")
		
		printG("All assets prepared.", "green")
		
		
		# Draw time
		# Reserve area under time for clock
		printG("Generating time...", "blue")
		
		maxclockheight = round((55*pixelratio)+(50*pixelratio))
		maindraw.rectangle([(0,0),(resx, maxclockheight)], fill=colors[3])
		
		maindraw.text((10*pixelratio,0), strftime("%I:%M"), fill=colors[1], font=fonts[0]) #Hour
		maindraw.text((150*pixelratio,10*pixelratio), strftime("%p"), fill=colors[1], font=fonts[1]) #AM/PM
		maindraw.text((10*pixelratio, 55*pixelratio), strftime("%A, %b %d, %Y"), fill=colors[0], font=fonts[2]) #Date
		
		printG("Generated: Time", "green")
		
		
		# Draw cards
		# Determine total number of cards
		printG("Calculating spaces...", "blue")
		cardsx = math.floor(resx/pixelratio/100)
		cardsy = math.floor((resy-maxclockheight)/pixelratio/100)
		printG("This SmartFrame (" + str(resx) + "x" + str(resy)+ ") can fit a " + str(cardsx) + "x" + str(cardsy) + " grid of cards.", "yellow")
		cardarray = [[False for x in range(cardsx)] for y in range(cardsy)] # False = unused, True = used
			
		nocards = False
		# Loop through each x and y.
		for y in range(0, cardsy):
			for x in range(0, cardsx):
				# If there are no more cards, stop finding places for them
				if len(cards) == 0:
					printG("Out of cards! Generation complete!", "green")
					nocards = True
					break
			
				# If space is filled or out of range, move to next space.
				try:
					if cardarray[y][x]:
						printG("("+str(x)+", "+str(y)+") is filled!")
						continue
				except IndexError:
					printG("("+str(x)+", "+str(y)+") is out of range!")
					continue
				# If space is not filled:
				else:
					#printG("("+str(x)+", "+str(y)+") is empty!")
					currentcard = ""
					enoughspace = True
					# Loop through all cards to find one that fits
					for i, currentcard in enumerate(cards):
						currentcardrange = "[ (" + str(x) + ", " + str(y)+"), (" + str(x+currentcard.tilesx-1) + ", " + str(y+currentcard.tilesy-1) + ") ]"
						printG("Trying card ["+str(i)+"] " + currentcard.sourcename + " with size ("+ str(currentcard.tilesx) + ", " + str(currentcard.tilesy)+ ") in area " + currentcardrange + "...", "blue")
						used = False
						for cardy in range(y,y+currentcard.tilesy):
							for cardx in range(x,x+currentcard.tilesx):
								try:
									if cardarray[cardy][cardx]:
										# If card doesn't fit, try next card
										used = True
								except IndexError:
									# If card is too big, try another card
									printG("("+str(cardx)+", "+str(cardy)+") is out of range! Stopping check...")
									used = True
								if used:
									printG("("+str(cardx)+", "+str(cardy)+") is filled! Stopping check...")
									break
							if used:
								break
						if not used:
							break
						if used and i == len(cards)-2:
							enoughspace = False    
					if not enoughspace:
						# If there's not enough space for any card, iterate to next space:
						printG("Not enough space for any card in (" + str(x) + ", " + str(y) + ")!", "red")
						continue
					else:
						printG("All space for card " + currentcard.sourcename + " is empty! Stopping check...", "green")
						
						# set target cells to filled
						printG("Setting range " + currentcardrange + " to filled...")
						for cardy in range(y, y+currentcard.tilesy):
							for cardx in range(x, x+currentcard.tilesx):
								cardarray[cardy][cardx] = True
						for line in cardarray:
							print(str(line))
						
						# place card!
						printG("Placing card " + currentcard.sourcename + " at " + currentcardrange + "...", "blue")
						xstart = x*(100*pixelratio)
						ystart = y*(100*pixelratio)+maxclockheight
						xend = (pixelratio*(100)*currentcard.tilesx)+xstart
						yend = (pixelratio*(100)*currentcard.tilesy)+ystart
						#maindraw.rectangle([(xstart,ystart),(xend, yend)], fill=colors[4], outline=colors[0], width = round(2*pixelratio)) # Debug
						image = currentcard.Image(xend-xstart, yend-ystart)
						mainimage.paste(image, (round(xstart),round(ystart)))
						
						# pop card from array!
						printG("Card placed successfully! Removing from array...", "green")
						cards.pop(cards.index(currentcard))
						printG("There are " + str(len(cards)) + " cards remaining...", "yellow")
			if nocards:
				break
	
	
		# Alt text / overflow
		alttext = ""
		if len(cards) != 0:
			alttext = cards[0].sourcename + ": " + cards[0].alttext
			if len(cards) > 1:
				remainingcards = len(cards)
				if remainingcards > 1:
					alttext+=" and " + str(remainingcards) + " more cards"
				else:
					alttext+=" and 1 more card"
			printG("Some cards remaining! Setting alttext to \"" + alttext + "\"")
		if alttext:
			maindraw.rectangle([(0,resy-(30*pixelratio)-5),(resx, resy)], fill=colors[3])
			maindraw.text((10*pixelratio, resy-(30*pixelratio)), alttext, fill=colors[2], font=fonts[3])
		
		# Done!
		printG("Image generated!", "green")
		return mainimage
	except KeyboardInterrupt:
		print("Keyboard interrupt detected! Exiting...")
		exit(0)
	except:
		import traceback
		logError("There was an error!" + file + "!", traceback.format_exc(), moduleName)
		return mainimage



# ~~~Test code~~~
#from PIL import Image, ImageFont, ImageDraw
#from Card import Card
#from time import gmtime, strftime
#import os
#import math
#files = os.listdir("Cards")

#cards = [Card(files[0], "poggers", files[0], 2, 2),
		 #Card(files[1], "poggers", files[1], 4, 4),
		 #Card(files[2], "poggers", files[2], 4, 2),
		 #Card(files[3], "poggers", files[3], 1, 1)]
	
#GenerateImage(cards, 720, 1280, 4).show()
#GenerateImage(cards, 1080, 1920, 8).show()
#GenerateImage(cards, 1920, 1080, 24).show()