#!/usr/bin/python3
# RaddedMC's SmartFrame v2 -- ErrorLogger.py
# Logs errors from other files

from termcolor import colored
from datetime import datetime

def getLogLocation():
	file = __file__.replace('\\', '/') # Remove this if you use a specific file path for your image or some other method.
	index = file.rfind("/")
	file = file[:index]
	logFilePath = file + "/" + "SmartFrame.Error.Log.TXT" # File location of image
	return logFilePath
	
def logError(errorHeader, traceback, moduleName):
	print(moduleName + " | " + colored(str(errorHeader), "red"))
	print(traceback)
	try:
		with open(getLogLocation(), "a") as logfile:
			now = datetime.now()
			logfile.write(moduleName + " @ " + now.strftime("%H:%M:%S %d/%m/%Y") + " | " + errorHeader + "\n")
			logfile.write(traceback + "\n")
	except:
		print("Error Logger | " + colored(str("Error writing log to file!"), "red"))
		import traceback
		traceback.print_exc()