#!/bin/python3
# RaddedMC's SmartFrame v2 -- NewCovidCasesMLHU.py by @Raminh05
# This is a plugin to display daily new covid cases in the region of Middlesex-London, Ontario, Canada.
# Middlesex-London COVID data from the Middlesex-London Health Unit.
# This particular template will let you show a single large number and some small text with a fancy background.

# Required deps for NewCasesMLHUCovid: Pillow, termcolor, requests, datetime, openpyxl.

# No need to define any user variables! It just works. 

# Add any user-definable variables here! (API keys, usernames, etc.)
sourcename = "NewCasesCasesMLHU"

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import math

SMARTFRAMEFOLDER = ""
COLORS = []

#### YOUR CODE HERE ####
def GetCardData():
    count = 21
    maintext = "Some data"
    alttext = "Whatever you want!"

    # -- Import modules -- #
    import requests
    from openpyxl import load_workbook
    from datetime import datetime

    # Fetches excel file from MLHU
    def get_response(excel_url):
        response = requests.get(excel_url)

        if response.status_code == 404: # If the plugin fails to get data
            printC("Failed to fetch excel file. Sending null to card.", "red")
            count = None
            maintext = None
            alttext = None
            raise NameError("MLHU has not updated the excel file for today.") # Crashes the plugin
        else:
            printC("Sucessfully fetched excel file.", "green")
            with open("london_covid.xlsx", 'wb') as f:
                f.write(response.content)
                f.close()
                printC("Finished writing contents. Moving on to parsing.", "green")

    # Parses excel file, gets case data
    def parse_response():
        wb = load_workbook("london_covid.xlsx")
        worksheet = wb["Daily status"]
        xlsx_date = worksheet["A4"].value
        new_cases = worksheet["B15"].value

        return xlsx_date, new_cases

    now = datetime.now()
    time = now.strftime("H%:M%")
    date = now.strftime("%Y-%m-%d")
    excel_url = "https://www.healthunit.com/uploads/summary_of_covid-19_cases_in_middlesex-london_" + date + ".xlsx"

   # -- Only run this plugin at 3PM -- #
    if time == "15:00":
        response = get_response(excel_url) # Updates data to the xlsx file
        count = parse_response()[1]
    else: # -- If not 3PM -- #
        printC("Not 3PM yet. Looking to see if you have the most current COVID data...", "yellow")
        try:
            xlsx_date = parse_response()[0].strftime("%Y-%m-%d") # Fetches latest date from the xlsx. Fails if no xlsx -> except below
            if date != xlsx_date: # If not 11 AM but xlsx is out of date (!= to irl date), update.
                printC("You do not have the latest COVID-data. Updating data now...", "yellow")
                get_response(excel_url)
                count = parse_response()[1]
                printC("Sucessfully fetched new data!", "green")
            else:
                printC("Your COVID data is up-to-date. Returning that to the card.", "green")
                count = parse_response()[1]
        except: # -- If there's no xlsx file present -- #
            printC("No london_covid.xlsx file is found! Downloading one right now...", "yellow")
            get_response(excel_url)
            count = parse_response()[1]

        maintext = "New\nMiddlesex-London\nCOVID Cases Today" # Spaces to fix centering
        alttext = "There are " + str(count) + " new cases of COVID-19 in Ontario today."

    return count, maintext, alttext
#### YOUR CODE HERE ####

def GenerateCard():
    # EDIT THESE TO CUSTOMIZE YOUR PLUGIN'S APPEARANCE!
    tilesX = 2 # I don't recommend changing these values for this template
    tilesY = 2 # I don't recommend changing these values for this template
    dpifactor = 200 # Change this to increase card resolution. Don't go too high!!!
    backgroundcolor = COLORS[3] # Change this to a 3-value tuple (255, 200, 100) to change the background colour!
    textcolor = COLORS[1] # Change this to a 3-value tuple to change the text colour!
    circlesbgcolor = (COLORS[3][0]-10, COLORS[3][1]-10, COLORS[3][2]-10) # Change this to a 3-value tuple to change the background color of your progress meter!
    printC("Counter circles background color is " + str(circlesbgcolor))

    imageresx = tilesX*dpifactor
    imageresy = tilesY*dpifactor
    image = Image.new("RGB", (tilesX*dpifactor, tilesY*dpifactor))
    imagedraw = ImageDraw.Draw(image)
    imagedraw.rectangle([(0,0), (imageresx, imageresy)], fill=backgroundcolor)

    count, maintext, alttext = GetCardData()

    if maintext and alttext:
        maintextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 10*round(dpifactor/50))
        if count in range(0, 1000): # Don't worry i hate this too
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 45*round(dpifactor/50)) # Change specifically made to fit this plugin
        elif count < 1000:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 40*round(dpifactor/50))
        elif count < 10000:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 35*round(dpifactor/50))
        elif count < 100000:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 30*round(dpifactor/50))
        else:
            counttextfont = ImageFont.truetype(SMARTFRAMEFOLDER + "/Fonts/font1.ttf", 20*round(dpifactor/50))

        # Logarithm
        try:
            logAmt = math.log((count),10)
        except ValueError:
            logAmt = 1
        if logAmt == 0:
            logAmt = 1
        printC("LogAmt is " + str(logAmt))

        # Top position
        topdivamt = (128/(5*logAmt))
        if topdivamt < 3:
            topdivamt = 3
        counttexttop = imageresx/topdivamt

        # Start position
        startdivamt = (2.2*logAmt)+3
        if count < 10:
            startdivamt = 3
        counttextstart = imageresx/startdivamt

        printC("Counter scale factors are (" + str(startdivamt) + ", " + str(topdivamt) + ")")

        # Circles
        cols = math.ceil(math.sqrt(count))
        rows = round(math.sqrt(count))
        printC("Generating a ("+str(cols)+"x"+str(rows)+") grid of " + str(count) + " circles...")

        padding = imageresx/(4*cols)
        size = (imageresx/cols) - padding
        for i in range(0,count):
            col = i % cols
            row = math.floor(i/cols)
            xpos = (padding/2)+(size+padding)*col
            ypos = (padding/2)+(size+padding)*row
            imagedraw.ellipse((xpos, ypos, xpos+size, ypos+size), fill=circlesbgcolor)

        imagedraw.text((dpifactor/50,3*imageresy/5), maintext, font=maintextfont, fill=textcolor)
        imagedraw.text((counttextstart, counttexttop), str(count), font=counttextfont, fill=textcolor) # Counter text
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

