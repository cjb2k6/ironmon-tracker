# README #

### IronMON Tracker for Generation 1 and 2 Pokémon games ###

This is a Pokémon stat tracker designed to be used for the [IronMON](https://gist.github.com/valiant-code/adb18d248fa0fae7da6b639e2ee8f9c1) challenge.
The program utilizes a LUA script that runs in the BizHawk emulator in order to extract information from the game's
RAM and displays it in a separate window written in Python.

* The tracker always displays the following information
  * Lead Pokémon Information
    * Pokémon Nickname or Name
    * Type
    * Current Level / Evolves At
    * Current HP / Total HP
    * Number of Moves Learned / Total Moves Learnable
    * Level of Next Learned Move
    * Total Percentage of Heals / Total Number of Healing Items in Bag
    * Current Held Item (Gen 2)
    * Stats and Base Stat Total
  * Lead Pokémon Moves
    * Move Name
    * Type
    * Current PP
    * Power
    * Accuracy


* The tracker conditionally shows the following information
  * Number of attempts at challenge (Enabled in Settings)
  * Three Favorite Pokémon sprites (Enabled in Settings)
  * Enemy Pokémon Information (In Battle)
    * Name
    * Level
    * Base Stat Total
    * Type
  * Wild Pokémon Information (In Battle, including enemy info from above)
    * Number of Moves Learned / Total Moves Learnable
    * Level of Next Learned Move
    * Evolves At


### Setup ###

* Download the latest release of this tracker and extract all files to a folder
* Download [BizHawk](https://tasvideos.org/Bizhawk) emulator
* Install [Python](https://www.python.org/downloads/) version 3.8 or later
* Install Python Dependencies
  * For Windows users, run the Setup_Windows.bat file
  * For other platforms, run the following terminal commands from the tracker's root directory
    * >pip install pygame
    * >pip install numpy
      
### First Time Run ###

* Run the tracker to ensure it works. This will also generate some more files
  * For Windows users, run the Start_Tracker_Windows.bat file
  * For other platforms, run the following terminal command from the tracker's root directory
  * >python tracker.py
* If successful, you should see the tracker with no data filled out
* Close the tracker for now

### Using the Tracker ###

* Open BizHawk and load your game ROM file
  * Tracker supports the following games, only English ROMs have been tested
    * Pokémon Red Version
    * Pokémon Blue Version
    * Pokémon Yellow Version
    * Pokémon Gold Version
    * Pokémon Silver Version
    * Pokémon Crystal Version
* In BizHawk, select Tools from menu bar and then select Lua Console
  * In the Lua console, select Script from menu bar then select Open Script
    * Navigate to the folder containing the tracker files and open one of the two Lua scripts
      * gen1.lua for Pokémon Red, Blue, and Yellow
      * gen2.lua for Pokémon Gold, Silver, and Crystal
  * Upon loading, there should be a message in the Lua console with your game version
* Open the Tracker using the same bat file or command from the First Time Run

### Configuring the Tracker ###

* Keybinds and Settings

Key Combination | Action
------------- | -------------
Ctrl+Q  | Close Tracker Program
Equals OR NumPad-Plus  | Increment Attempts
Minus OR NumPad-Minus  | Decrement Attempts
Ctrl+R OR Ctrl+NumPad-0 | Reset and Increment Attempts
Ctrl+M  | Load random mail message
Ctrl+S  | Save current mail message to file

### Mail Randomizer ###

* Mail Stuff