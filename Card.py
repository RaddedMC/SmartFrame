# RaddedMC's SmartFrame v2 -- Card.py

# Required deps: PIL

#   fileLocation -- The location of the image attached to this object. Used in Image()
#                    JUST GIVE THE IMAGE's FILENAME. Card.Image() will do all the heavy lifting.
#   alttext      -- Alternate text for the image that contains basic data.
#   sourcename   -- The name of the source that generated the Card.
#   Image()      -- returns a PIL image generated from fileLocation.
#   tilesX       -- returns width of image in tile units. (200 pixels per unit)
#   tilesY       -- returns height of image in tile units.

# Recommended card sizes:
#  -- 1x1, single icon
#  -- 2x2, icon and some text
#  -- 4x2, long text
#  -- 4x4, a lotta data


class Card:

    fileLocation = ""
    alttext = ""
    sourcename = ""
    tilesx = 2
    tilesy = 2

    def __init__(self, fileLocation, alttext, sourcename, tilesx, tilesy):
        self.fileLocation = fileLocation
        self.alttext = alttext
        self.sourcename = sourcename
        self.tilesx = tilesx
        self.tilesy = tilesy
        print("New Card | " + sourcename + "'s card at " + fileLocation + " | Size: " + str(tilesx) + "x"+str(tilesy) + " | " + alttext)
        
    def __str__(self):
        return "Card object: " + self.sourcename + "'s card at " + self.fileLocation + " | Size: " + str(self.tilesx) + "x"+str(self.tilesy) + " | " + self.alttext
    
    def Image(self, sizex=200, sizey=200):
        from PIL import Image
        import os
        imgdir = os.getcwd().replace('\\', '/')+"/Cards/"+self.fileLocation
        image = Image.open(imgdir)
        image = image.resize((round(sizex), round(sizey)))
        return image