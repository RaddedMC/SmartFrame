# RaddedMCs SmartFrame
This project is still a work in progress.

**Welcome to my SmartFrame repo! This program is designed to grab your favourite data from all over the internet (Smart Home, Spotify, Weather/COVID data, etc) and display it in a neatly formatted image.**
You can use SmartFrame to send data to displays like a digital photo frame (https://youtu.be/YDr95xaEsK4), your phone (iOS shortcut planned), or other infoboard-type devices.

**IF YOU ARE INTERESTED IN MAKING A PLUGIN,** scroll to the bottom of this readme file :D

## Community:
Thanks to everyone who has helped my community and this project grow! Huge shoutouts to:
* @Raminh05: Plugin development and Linux testing
* @kelvinhall05: Literature writing, General cringe, and Linux testing
* **Friendly Fire Entertainment**: Advice for the original SmartFrame hardware

[Editor.md](https://pandao.github.io/editor.md/en.html "Editor.md") for making this readme file faster to make

If you want to get involved in this project or any of my other projects, come hang out on the `#nerdery` channel on my Discord:
https://discord.gg/9Ms4bFw

If you want to see my other projects, check out my GitHub page or YouTube channel:
https://github.com/RaddedMC
https://youtube.com/c/RaddedMC

Other ways to hang out:
https://instagram.com/RaddedMC
https://linktr.ee/RaddedMC


## Setup:
#### Start by cloning the repo and installing the dependencies.
### Dependencies:
All dependencies can be installed with `pip install $`
* Pillow (primary image library)
* termcolor (fancy logging colours)
* pandas (fancy grid output for GenerateImage)
* console-menu (user-friendly interface for configuring SmartFrame)

------------
#### Next, setup your config file.
### Config file
- cd into the repo and run SmartFrame `python3 SmartFrame.py`
- Follow the steps to create a config file
- Once the config file is created, set up your output sources!

#### Syntax:
* Every entry starts with an output resolution and scale factor in the form of `1080x1920s4`.
   * Where `1080` is the horizontal resolution, `1920` is the vertical resolution, and `4` is the scale factor.
   * A larger scale factor means more cards on the screen and smaller text.
* On a **new line**, type the full file path that you want the image to output to.
   * Ex: C:\Users\Owner\Desktop\SmartFrameIMG.jpg
   * Or: /home/pi/SmartFrameIMG.jpg
   * \*It does not matter if you are using Windows or Linux\*. Just type the file path how you normally would.
* **Optional:** Add before / output commands
   * The user that runs these commands entirely depends on how you run SmartFrame.py.
   * If you run SmartFrame.py as administrator/root, these commands will run as administrator/root.
   * On a **new line**, type one or two commands to run.
      * If you type one command, it will be run after generating and saving the photo.
	  * If you type type two commands, the first one will be run after generating/saving the photo, and the second will be run before generating/saving the photo.
* **Optional:** Have SmartFrame delete the outputted image when finished running commands.
	* On a **new line**, type the word `delete`.
* When adding multiple entries, separate them with a *hashtag*  `#` on another new line.

#####Example config file entry:
```
1080x1920s8
R:\Dev\Python\SmartFrameV2\SmartFrame1080.png
./ThingToDoAfterGenerating.sh
./ThingToDoBeforeGenerating.sh
delete
#
```
#####Example config file:
```
# Refresh time (seconds): Higher is better to prevent API spam, lower gives more up-to-date info
60
# Use this area to set up output types. Start with the output resolution in the form 1920x1080s4, where 4 is the scale factor..
# On a new line, write the full file output path.
# On another line, write a command to run after generating the photo.
# On another line, write a command to run before generating the photo.
# If you only add one command, it will run after generating the photo.
# Finally, write 'delete' on another line at the end of your entry if you want the file to be deleted after the 'after' command is ran.
# Use a hashtag on a newline to seperate output entries.
# Ex:
# 1920x1080s4
# /home/RaddedMC/SmartFrame1080.png
# bash /home/RaddedMC/Scripts/SmartFrameOut.sh
# bash /home/RaddedMC/Scripts/SmartFrameIn.sh
# delete
# #
1080x1920s8
R:\Dev\Python\SmartFrameV2\SmartFrame1080.png
```
**Do not delete the instruction text in the config file, as it will break the file.** I know that this is stupid and my interpreter should interpret better. This will be changed in the future when I start polishing the project further.


------------
#### Set up your theme!
### Theming:
To change the appearance of your SmartFrame, edit the `colors.txt` and `Fonts/font1.ttf` file:
Note that not all plugins may follow your theme.
##### Colors:
Use [Adobe Color](https://color.adobe.com/ "Adobe Color") or some other method to get 4 colors for colors.txt.
* Color 1: Date text color
* Color 2: Clock text color
* Color 3: Overflow text color (bottom bar)
* Color 4: Background color
These colors need to be in RGB form, as they appear in the file.

##### Fonts:
Simply take your favourite TTF font and copy it into the `Fonts/` folder, then rename it to `font1.ttf`.
The default font is 8-bit Operator, available here: https://www.dafont.com/pixel-operator-old2.font

------------
#### Add plugins!
### Plugins:
Check out the `Available Plugins/` folder for plugins that RaddedMC and other developers have worked on.
Pick your favourites, and drag-drop the files within their subfolders into your `Plugins/` folder.
Make sure to follow instructions for your plugins of choice before just running SmartFrame.

------------
#### Finally, run SmartFrame.py to test, then setup a cronjob or other scheduled task and you're good to go!

------------
### For plugin developers:
More instructions will come soon, but please feel free to use one of the templates in `Plugin Templates/` to get started.
When you are ready to add your plugin to SmartFrame, create a pull request or message me on [Discord](https://discord.gg/9Ms4bFw)!