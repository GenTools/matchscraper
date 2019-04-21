# Matchscraper

A script for finding the occurence of surnames among an Ancestry DNA match and their shared matches.

## Setup

1. Install Python (version 2.7 or newer) if you don't have it already.

2. Install Selenium library for Python. From command line, "pip install selenium" (you might need to install pip first).

3. Install ChromeDriver https://sites.google.com/a/chromium.org/chromedriver/downloads 
(you'll need to have Chrome installed as well). 

Instructions for installing ChromeDriver for Windows:
http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/

For macOS:
https://www.kenst.com/2015/03/installing-chromedriver-on-mac-osx/

4. Download matchscraper.py script from this page and put it where you want it. (You might want to create an alias or put it in your PATH.)

## Use

1. Run it from command line with "python matchscraper.py". 

2. Enter your Ancestry username and password when prompted (this goes straight to the Ancestry website, no one else sees it). 
If you want, you can put your username and/or password inside the empty quotes under '''configuration data''' in the 
matchscraper.py file. That way you won't have to enter it every time you run the script. 

3. Enter the url of the match you're interesed in. This should be for the page where you see the match's tree and the list of surnames on the left.

4. It might take a couples minutes to run. When finished, it will create a text file with your match's name in the title.
The text file will contain three columns. The first contains all the surnames that occur in the tree of your match and 
in the trees of the matches you share with that match. The second shows the number of trees each surname appears in. 
The third lists the names of the matches that have the surname in their tree. 

## Tips

1. Try not to run too much within a short period of time. It taxes the servers, and they could potentially try to block you.
