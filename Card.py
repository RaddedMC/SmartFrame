# RaddedMC's SmartFrame v2 -- Card.py

# Required deps: PIL

#   fileLocation -- The location of the image attached to this object. Used in Image()
#   alttext      -- Alternate text for the image that contains basic data.
#   sourcename   -- The name of the source that generated the Card.
#   Image()      -- returns a PIL image generated from fileLocation.
#   tilesX       -- returns width of image in tile units. (200 pixels per unit)
#   tilesY       -- returns height of image in tile units.

# Recommended card size:
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
        print("New Card | " + sourcename + "'s card at " + fileLocation + " | Size: " + str(tilesx) + "x"+str(tilesy) + " | " + alttext)
        
    def Image():
        from PIL import Image
        return Image.open(fileLocation)