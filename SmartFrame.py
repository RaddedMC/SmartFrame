#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- SmartFrame.py
# This program is the primary wrapper for SmartFrame v2!

# Options
#   -h / --help        = Runs help() and quits
#   -c                 = Asks user to confirm and if yes, clears configfile
#   -j                 = Just get data

# Title()       -- Prints the epic title screen
# ClearConfig() -- Asks for confirmation and then clears the user's config file.
# Config()      -- Displays the config menu
# ReadConfig()  -- Reads in the config file
# ConfigFileError(error) -- Displays a screen asking the user if they want to correct an error in their config file.
# GetCardData() -- Returns a Card array

# printS()      -- just a simple output formatter

# Required deps: console-menu, termcolor
# KEY FILES: config.cfg
#            Plugins/

builddate = "2021 - 08 - 12"
moduleName = "SmartFrame Main"

# Imports
import os, time, sys
from consolemenu import *
from consolemenu.items import *
from Card import Card
from GenerateImage import GenerateImage
from datetime import datetime
from datetime import timedelta
from ErrorLogger import logError
import multiprocessing


def printS(string, color = "white"):
	from termcolor import colored
	print(moduleName + " | " + colored(str(string), color))


refreshtime = -1
# Config object
class Output:
	# Xres
	xres = 0
	
	# Yres
	yres = 0
	
	# scalefactor
	scale = 0
	
	# outputlocation
	outputlocation = ""
	
	# Introcommand
	introcommand = ""
	
	# Outrocommand
	outrocommand = ""
	
	# delete boolean
	todelete = False
	
	def __init__(self, xres, yres, scale, outputlocation = "", outrocommand = "", introcommand = "", todelete = False):
		self.xres = xres
		self.yres = yres
		self.scale = scale
		self.outputlocation = outputlocation
		self.outrocommand = outrocommand
		self.introcommand = introcommand
		self.todelete = todelete
		outputstr = "New Output Config | will output a " + str(self.xres) + "x" + str(self.yres) + "s" + str(self.scale) +" image to " + self.outputlocation + " "
		if self.introcommand != "":
			outputstr += "after running " + self.introcommand + " "
		if self.outrocommand != "":
			outputstr += "before running " + self.outrocommand + ". "
		if self.todelete:
			outputstr += "The output will be deleted."
		print(outputstr)
	
	def __str__(self):
		outputstr = "Output config object: will output a " + str(self.xres) + "x" + str(self.yres) + "s" + str(self.scale) + " image to " + self.outputlocation + " "
		if self.introcommand != "":
			outputstr += "after running " + self.introcommand
		if self.outrocommand != "":
			outputstr += "before running " + self.outrocommand + "."
		if self.todelete:
			outputstr += "The output will be deleted."
		return outputstr


def ConfigFileError(error = "Unknown error in config file!"):
	openmenu = SelectionMenu("")
	fixerrorchoice = openmenu.get_selection(["Reset config and exit"], "Error!",  error+"\nWould you like to correct this yourself or delete the config file and start from scratch?")
	if fixerrorchoice == 0:
		ClearConfig()
		exit()
	else:
		exit()

# Fancy title screen
def Title():
	try:
		widthlimit = os.get_terminal_size().columns
	except OSError:
		printS("Unable to get terminal width. We are not running in a console.")
		return None
	print("\nSmartFrame | Options [-h / -c / -j / -t]\n")
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
	print(("{0:>"+str(widthlimit)+"}").format("@Raminh05 -- Plugin development and Linux testing"))
	time.sleep(0.1)
	print(("{0:>"+str(widthlimit)+"}").format("@kelvinhall05  -- Literature writing, General cringe, and Linux testing"))
	time.sleep(0.1)
	print(("{0:>"+str(widthlimit)+"}").format("@Friendly Fire Entertainment  -- Advice for RaddedMC's SmartFrame hardware"))
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
	

def ReadConfig():
	try:
		printS("Reading config file...", "blue")
		configfile = open("config.cfg", 'r')
		configlines = configfile.readlines()
		for index, line in enumerate(configlines):
			configlines[index] = line.strip()
		printS("Config file opened!", "green")
		
		printS("Parsing configfile...", "blue")
		printS("Getting refresh time...", "blue")
		# Get refresh time
		try:
			global refreshtime
			refreshtime = int(configlines[1])
		except ValueError:
			configfile.close()
			ConfigFileError("It looks like your refreshtime is an invalid value. You have set it to: " + configlines[1] + ". This needs to be a number in seconds.")
		except KeyboardInterrupt:
			print("Keyboard interrupt detected! Exiting...")
			exit(0)
		printS("Refresh time is " + str(refreshtime) + " seconds!", "green")
		
		printS("Setting up output objects...", "blue")
		startdex = 16
		outputObjects = []
		while True:
			printS("Starting at line "+ str(startdex) + " of config file...", "yellow")
			currentXres = 0
			currentYres = 0
			currentScale = 0
			currentOutputLocation = ""
			currentCommands = []
			currentToDelete = False
			# If the startdex does not exist or is empty, break loop!
			try:
				if configlines[startdex] == "" or not configlines[startdex]:
					break
			except IndexError:
				break
			except KeyboardInterrupt:
				print("Keyboard interrupt detected! Exiting...")
				exit(0)
			# Otherwise, first line of startdex is resolution
			splitdex = configlines[startdex].find("x")
			scaledex = configlines[startdex].find("s")
			currentXres = configlines[startdex][:splitdex]
			currentYres = configlines[startdex][splitdex+1:scaledex]
			currentScale = configlines[startdex][scaledex+1:]
			# Second line is output location
			currentOutputLocation = configlines[startdex+1]
			
			# If any of these lines aren't 'delete' or '#':
			finaldex = 2
			for line in configlines[startdex+2:startdex+6]:
				if line == "#":
					finaldex+=1
					break
				if line == "delete":
					currentToDelete = True
				else:
					currentCommands.append(line)
				finaldex += 1
			try:
				outputObjects.append(Output(currentXres, currentYres, currentScale, currentOutputLocation, currentCommands[0], currentCommands[1], currentToDelete))
			except IndexError:
				try:
					outputObjects.append(Output(currentXres, currentYres, currentScale, currentOutputLocation, currentCommands[0], "", currentToDelete))
				except IndexError:
					outputObjects.append(Output(currentXres, currentYres, currentScale, currentOutputLocation, "", "", currentToDelete))
				except KeyboardInterrupt:
					print("Keyboard interrupt detected! Exiting...")
					exit(0)
			except KeyboardInterrupt:
				print("Keyboard interrupt detected! Exiting...")
				exit(0)
				
			startdex+=finaldex
		
		printS("Finished reading config file!", "green")
		return outputObjects
	except KeyboardInterrupt:
		print("Keyboard interrupt detected! Exiting...")
		exit(0)
	except:
		ConfigFileError("There was an error loading your config file! Double check your file or report an issue on the github!")
		import traceback
		traceback.print_exc()
		exit()


# Creates a new config file
def Config():
	config = ""
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
			0: "60\n",
			1: "360\n",
			2: "30\n",
			3: "0\n",
			4: "exit"
		}
		if not options.get(menchoice) == "exit":
			config += "# Refresh time (seconds): Higher is better to prevent API spam, lower gives more up-to-date info. NOTE: No matter your Refresh Time, SmartFrame cannot run faster than your plugins can generate information. This value simply affects the sleep timer at the end of generating a photo.\n"
			config += options.get(menchoice)
			
			config += "# Use this area to set up output types. Start with the output resolution in the form 1920x1080s4, where 4 is the scale factor..\n"
			config += "# On a new line, write the full file output path.\n"
			config += "# On another line, write a command to run after generating the photo.\n"
			config += "# On another line, write a command to run before generating the photo.\n"
			config += "# If you only add one command, it will run after generating the photo.\n"
			config += "# Finally, write 'delete' on another line at the end of your entry if you want the file to be deleted after the 'after' command is ran.\n"
			config += "# Use a hashtag on a newline to seperate output entries.\n"
			config += "# Ex:\n"
			config += "# 1920x1080s4\n"
			config += "# /home/RaddedMC/SmartFrame1080.png\n"
			config += "# bash /home/RaddedMC/Scripts/SmartFrameOut.sh\n"
			config += "# bash /home/RaddedMC/Scripts/SmartFrameIn.sh\n"
			config += "# delete\n"
			config += "# #\n"
			
			file = open("config.cfg", "w")
			file.write(config)
			file.close()
			
			print("You can now open your favourite text editor to edit " + os.getcwd().replace('\\', '/')+"/config.cfg"+" and finish configuration.")
			
		# Output resolutions / companion outputters
	
	print("Run SmartFrame again to get started.")

def runPlugin(file, send_end):

	# Get and run modules
	import importlib.util
	from io import StringIO
	spec = importlib.util.spec_from_file_location("module.name", "Plugins/" + file)
	plugin = importlib.util.module_from_spec(spec)
	
	printS("Starting plugin " + file, "cyan")
	
	# Capture stdout to keep plugin output organized
	sys.stdout = stdoutStream = StringIO()
	
	# Check for compile errors
	try:
		spec.loader.exec_module(plugin)
		
		# Run plugin
		try:
			plugincards = plugin.GetCard()
		except:
			import traceback
			logError("Runtime error with plugin " + file + "!", traceback.format_exc(), moduleName)
			plugincards = None
		
	except:
		import traceback
		logError("There's a compiler error with plugin " + file + "! Contact the developer for this plugin or fix the error yourself and make a pull request." + file + "!", traceback.format_exc(), moduleName)
		plugincards=None
		
	finally:
		# Regardless of whether everything works, return what you can, print what was outputted (including errors), and give back stdout
		printS("Plugin " + file + " finished!", "green")
		sys.stdout = sys.__stdout__
		print(stdoutStream.getvalue())
		send_end.send(plugincards)
	
# Main
def main():
	# Argument parsing
	import argparse
	parser = argparse.ArgumentParser(description="See https://github.com/RaddedMC/SmartFrame for more help.")
	parser.add_argument('-c', action="store_true", help = "Asks for confirmation and clears the config file")
	parser.add_argument('-j', action="store_true", help = "Just parses data from plugins, useful for testing")
	parser.add_argument('-t', action="store_true", help = "Skips the title screen :(")
	args = parser.parse_args()
	runonce = False
	
	# Show title screen
	if not args.t:
		Title()

	# Config file clearer
	if args.c:
		ClearConfig()
		
	# Runs SmartFrame only once
	if args.j:
		printS("SmartFrame will run once and exit.", "magenta")
		runonce = True
	
	# If the config file doesn't exist, make one!
	if not os.path.isfile('config.cfg'):
		Config()
		exit()
		
	configs = ReadConfig()
	
	printS("Starting main loop...", "cyan")
	### MAIN LOOP ###
	while True:
		# Get current time
		startGenTime = datetime.now()
		
		
		# Gather cards from plugins
		printS("Gathering cards...", "blue")
		
		cards = []
		files = os.listdir("Plugins/")
		
		# Get list of plugins in plugin folder and create processes for them
		tasks = []
		pipe_list = []
		if files:
			for file in files:
				if file.endswith(".py"):
					printS("Assembling plugin " + file, "yellow")
					recv_end, send_end = multiprocessing.Pipe(False)
					p = multiprocessing.Process(target=runPlugin, args=(file, send_end))
					tasks.append(p)
					pipe_list.append(recv_end)
					p.start()
					
		else:
			printS("Error: There are no plugins! Please add some plugins before using SmartFrame.", "red")
			exit(0)
			
		returnvalues = [x.recv() for x in pipe_list]
		
		for job in tasks:
			job.join()
			
		printS("All plugins finished! Assembling output...", "green")
		# Sort output from tasks
		for value in returnvalues:
			if isinstance(value, list):
				for card in value:
					cards.append(card) # Append all new cards to variable cards
			elif isinstance(value, Card):
				cards.append(value)
			else:
				continue
				
		printS("Cards assembled!", "green")
				 
		
		# Output images
		printS("Preparing outputs...", "blue")        
		for idx, config in enumerate(configs):
			try:
				# Run before scripts
				if (config.outrocommand):
					printS("Running " + config.introcommand + " ...", "blue")
					printS("Exit code: " + str(os.system(config.introcommand)), "green")
				
				# Generate images 
				printS("Generating image #" + str(idx) + "...", "blue")
				GenerateImage(cards, int(config.xres), int(config.yres), int(config.scale)).save(config.outputlocation.replace('\\','/'))
				
				# Run after scripts
				if (config.outrocommand):
					printS("Running " + config.outrocommand + " ...", "blue")
					printS("Exit code: " + str(os.system(config.outrocommand)), "green")
				
				# Clear cards
				if (config.todelete):
					printS("Deleting " + config.outputlocation + "...", "blue")
					os.remove(config.outputlocation)
					printS("Deleted " + config.outputlocation + "!", "green")
				
				printS("Image generated! Poggers!!!", "cyan")
			except KeyboardInterrupt:
				print("Keyboard interrupt detected! Exiting...")
				exit(0)
			except:
				import traceback
				logError("There was an error generating image #" + str(idx) + "! Double check your config file or report an issue on the github!", traceback.format_exc(), moduleName)
				continue
		
		
		# Delete card output images
		printS("Clearing cards...")
		for card in cards:
			os.remove(card.fileLocation)
			printS("Cleared card " + card.fileLocation)
		
		
		# Calculate sleep time
		#print(startGenTime)
		nowTime = datetime.now()
		#print(nowTime)
		#print(refreshtime)
		difference = timedelta(0,refreshtime)
		#print(difference)
		endTime = startGenTime + difference
		#print(endTime)
		sleepduration = (endTime - nowTime).total_seconds()
		#print(sleepduration)
		
		if runonce:
			printS("Finished! Exiting...", "green")
			exit(0)

		printS("Sleeping for " + str(sleepduration) + " seconds...", "yellow")
		if sleepduration > 0:
			time.sleep(sleepduration)


if __name__ == "__main__":
	main()
