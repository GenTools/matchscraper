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

## Use (Basic Mode)

1. Run it from command line with "python matchscraper.py". 

2. Enter your Ancestry username and password when prompted (this goes straight to the Ancestry website, no one else sees it). 
If you want, you can put your username and/or password inside the empty quotes under '''configuration data''' in the 
matchscraper.py file. That way you won't have to enter it every time you run the script. 

3. Enter the url of the match you're interesed in. This should be for the page where you see the match's tree and the list of surnames on the left.

4. It might take a couple minutes to run. When finished, it will create a CSV file with your match's name in the title. You can open the CSV file in excel. The file will contain three columns. The first contains all the surnames that occur in the tree of your match and in the trees of the matches you share with that match. The second shows the number of trees each surname appears in. The third lists the names of the matches that have the surname in their tree. 

## Group Mode

It is also possible to process multiple matches as a single group. 

1. Create a .csv file with four columns. In the first column, put the username of the match. In the second column, put a group name of your choice. In the third column, put a 'y' or 'yes' if you want the script to refrain from parsing the tree of this particular match (it will be excluded whether the match is a group member or is a a shared match of a group member). If you just want to exclude a match, fill in the third column and leave the second (group) column blank. If you don't want to exclude a group member, leave the third column blank or put 'n' in the field. In the fourth column, put in the URL of the match (the page that shows a preview of the match's tree). You can leave the fourth column blank for matches that you are just excluding.

2. Run matchscraper.py as in basic mode, except list the csv file afterwards as an argument. For example, if your group file is in the same directory, the command would be "python matchscraper.py ./groups.csv".

3. The program will generate two CSV files per group. The first is a list of surnames as in basic mode, except it lists the surnames as aggregated throughout the shared matches for every member of the group and excludes the parsing of all matches that have been marked in the exclude column. The second CSV is a list of all the shared matches with links to their pages.

## Tips

1. Try not to run too much within a short period of time. It taxes the servers, and they could potentially try to block you.

2. In group mode, use the exclude column to exclude all the matches for which you know how you are related. This will prevent their trees from generating false leads on other surnames. Also exclude close relatives of matches, such as children and siblings, as otherwise all the surnames in their tree will be counted an extra time.

3. Put all the matches whose MRCA is your brickwall ancestor into a single group with all of them marked 'yes' for exclude. Running in group mode will then give you a list of surnames drawing on all of your possible datapoints. 
