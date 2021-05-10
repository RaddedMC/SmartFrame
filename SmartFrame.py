#!/bin/python3
# RaddedMC's SmartFrame v2 -- SmartFrame.py
# This program is the primary wrapper for SmartFrame v2!

# Options
#   -h / --help        = Runs help() and quits
#   -c                 = Asks user to confirm and if yes, clears configfile
#   -j                 = Just get data

# Title()       -- Prints the epic title screen
# ClearConfig() -- Asks for confirmation and then clears the user's config file.
# Config()      -- Displays the config menu
# GetCardData() -- Returns a Card array

# Required deps: console-menu
# KEY FILES: config.cfg
#            Plugins/

builddate = "2021 - 05 - 10"

# Imports
import os, time
from consolemenu import *
from consolemenu.items import *

# Fancy title screen
def Title():
    widthlimit = os.get_terminal_size().columns
    print("\nSmartFrame | Options [-h / -c / -j]\n")
    print(("{0:<"+str(widthlimit)+"}").format("    SSS  MM   MM   AAA   RRR   TTTTT            |\               "))
    print(("{0:<"+str(widthlimit)+"}").format("   S     M M M M  A   A  R  R    T              | \              "))
    print(("{0:<"+str(widthlimit)+"}").format("    sSs  M  m  M  AaaaA  RrrR    T              |  }             "))
    print(("{0:<"+str(widthlimit)+"}").format("      S  M     M  A   A  R R     T              | /              "))
    print(("{0:<"+str(widthlimit)+"}").format("   SSS   M     M  A   A  R  R    T              |/               "))
    print(("{0:<"+str(widthlimit)+"}").format("           /|                 FFFF  RRR    AAA   MM   MM  EEEE   "))
    print(("{0:<"+str(widthlimit)+"}").format("          / |                 F     R  R  A   A  M M M M  E      "))
    print(("{0:<"+str(widthlimit)+"}").format("         {  |                 Fff   RrrR  AaaaA  M  m  M  Eeee   "))
    print(("{0:<"+str(widthlimit)+"}").format("          \ |                 F     R R   A   A  M     M  E      "))
    print(("{0:<"+str(widthlimit)+"}").format("           \|                 F     R  R  A   A  M     M  EEEE   "))
    print(("{0:<"+str(widthlimit)+"}").format("\_______________________________________________________________/"))
    time.sleep(0.5)
    print("By RaddedMC https://github.com/RaddedMC | https://youtube.com/RaddedMC | https://reddit.com/u/RaddedMC")
    print("      with help from BOX OF COOL PEEPS (https://discord.gg/9Ms4bFw)")
    time.sleep(0.5)
    print(("{0:>"+str(widthlimit)+"}").format("@Cannoli -- Plugin design"))
    time.sleep(0.1)
    print(("{0:>"+str(widthlimit)+"}").format("@Volvo  -- General cringe"))
    time.sleep(0.1)
    print(("{0:>"+str(widthlimit)+"}").format("@Friendly Fire Entertainment  -- Advice for SmartFrame hardware"))
    time.sleep(0.1)
    print(builddate+"\n")
    time.sleep(1.5)
    

cleared = False

# Asks for confirmation and clears the user's config file
def ClearConfig():
    
    # Set up menu
    print("Opening ClearConfig menu...")
    menu = ConsoleMenu("Clear Config File?", "Press 1 to delete your config file. This can't be restored later!")
    menu.append_item(FunctionItem("Delete config.cfg", DeleteConfig, should_exit=True))
    
    # Show menu
    menu.show()
    
    if not cleared:
        exit(0)
    
def DeleteConfig():
    try:
        os.remove('config.cfg')
    except FileNotFoundError:
        print("You don't have a config file! Let's make one...")
    cleared = True
    

config = " "
# Creates a new config file
def Config():
    print("Opening Config File Menu...")
    
    # Opening menu
    openmenu = SelectionMenu("")
    menchoice = openmenu.get_selection(["Let's go!"], "Welcome to SmartFrame!", "You're about to have a good time. Hopefully. SmartFrame starts out with a config file. Make one now?")
    
    if menchoice == 0:
        # Refresh time
        menchoice = openmenu.get_selection(["Every minute (recommended)", "Every 5 minutes (recommended for users with slow internet or a lot of plugins)", "Every 30 seconds (recommended on fast controllers)", "As fast as possible! (not recommended, will spam APIs)"],
                                        "Refresh time",
                                        "How often should SmartFrame refresh data and generate a new image?")
        options = {
            0: "1",
            1: "5",
            2: "0.5",
            3: "0",
            4: "exit"
        }
        if not options.get(menchoice) == "exit":
            config += "# Refresh time: Higher is better to prevent API spam, lower gives more up-to-date info\n"
            config += options.get(menchoice)
            
        # Output resolutions / companion outputters
    
    print(config)
    print("Run SmartFrame again to get started.")
    
    
# Main
def main():
    # Show title screen
    Title()
    
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(description="See https://github.com/RaddedMC/SmartFrame for more help.")
    parser.add_argument('-c', action="store_true", help = "Asks for confirmation and clears the config file")
    parser.add_argument('-j', action="store_true", help = "Just parses data from plugins, useful for testing")
    args = parser.parse_args()

    # Config file clearer
    if args.c:
        ClearConfig()
    
    # If the config file doesn't exist, make one!
    if not os.path.isfile('config.cfg'):
        Config()
        exit()
    
    # Once config file is made,
        # Loop for x seconds
        # Gather cards from plugins
        # Generate images
        # Run output scripts
        # Clear cards



if __name__ == "__main__":
    main()