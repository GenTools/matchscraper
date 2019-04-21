from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import time
import urllib2
import getpass

'''configuration data'''
username = ''
password = ''
isToCsv = True
isToTxt = False

'''global variables'''
unkCounter = 0
debug = False
exclusions = [] # names to exclude
excluded = [] # names encountered from exclusion list
url = ''

def logDbg(msg):
    global debug
    if debug == True:
        print msg

def processSurnames(driver, dict, matchName):
    for i in range(5):
        try:
            newPage = driver.find_element_by_class_name('surnameList')

            nameList = parseSurnames(newPage.text)

            '''add to global dictionary'''

            for name in nameList:
                if name == "no surnames found":
                    continue
                elif name not in dict:
                    dict[name] = [1, [matchName]]
                else:
                    dict[name][0] = dict[name][0] + 1
                    dict[name][1] = dict[name][1] + [matchName]

            print "Collected surnames for " + matchName
            break
        except Exception as e:
            time.sleep(1)
            logDbg("No surnames, try " + str(i))
            # print e

def parseSurnames(pageString):
    nameList = []
    lines = iter(pageString.splitlines())
    for line in lines:
        if line >= '0' and line <= '9':
            continue
        elif line.startswith('Surnames'):
            continue
        else:
            if ',' in line:
                line = line.replace(',', '')
            nameList.append(line.lower())

    return nameList

def processMatch(driver, dict):
    global excluded
    global unkCounter

    matchName = 'unknown'
    try:
        matchName = driver.find_element_by_xpath("//div[@class='matchNameWrap']").text
        if ")" in matchName:
            index = matchName.find(')')
            matchName = matchName[0:index+1]
            matchName = matchName.replace('\n', ' ')
        else:
            index = matchName.find('\n')
            matchName = matchName[0:index]
        print "Processing " + matchName
    except Exception as e:
        unkCounter += 1
        matchName = 'unknown' + str(unkCounter)
        print "Could not get match name from url: " + url

    try:
        el = driver.find_element_by_class_name('focus')

        opts = el.find_elements_by_tag_name('option')
        opts[1].click()

        logDbg("Found unlinked tree!")
    except:
        logDbg("No unlinked tree")

    if matchName not in exclusions:
        processSurnames(driver, dict, matchName)
    elif matchName not in excluded:
        excluded.append(matchName)

    exclusions.append(matchName)
    return matchName

def processSharedMatch(driver, url, dict):
    global unkCounter

    try:
        driver.get(url)

        time.sleep(7)

        processMatch(driver, dict)
    except Exception as e:
        print "Could not open url: " + str(e)

def toCsv(name, dict):
    outfile = open(name + "_ancestry_surnames.csv", "w")

    text = "SURNAME,OCCURRENCE,MATCH NAMES\n"
    for key, value in sorted(dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        text += key.capitalize() + "," + str(value[0]) + ","
        if value[1] is not None:
            for i in range(len(value[1])):
                text += value[1][i] + "; "
            text += "\n"
        else:
            text += "\n"
    outfile.write(text.encode('utf-8'))
    outfile.close()

def toTxt(name, dict):
    outfile = open(name + "_ancestry_surnames.txt", "w")

    outfile.write('{0:40}'.format("SURNAME") + "OCCURRENCE" + "\t" + "MATCH NAME(S)\n")
    for key, value in sorted(dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        outString = str(value[0]) + "\t\t"
        if value[1] is not None:
            for i in range(len(value[1])):
                outString += value[1][i] + "; "
            outString += "\n"
        else:
            outString += "\n"
        outfile.write('{0:40}'.format(key.encode('utf-8').capitalize()) + outString.encode('utf-8'))

    outfile.close()

def processPrimeMatch(driver, dict, matches, url):
    '''enter main match page'''
    if url != '':
        driver.get(url)

    time.sleep(7)

    driver.switch_to.default_content()

    matchName = processMatch(driver, dict)

    '''go to shared matches'''
    try:
        button = driver.find_element_by_xpath("//div[@class='matchesInCommonControl']/button[1]")
    except:
        print "Couldn't get shared matches. Wrong password? Wrong URL?"
        driver.quit()
        sys.exit()

    button.click()

    '''enter shared match page'''
    time.sleep(6)

    driver.switch_to.default_content()

    for i in range(0,20):
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            href = elem.get_attribute("href")
            if '?' in href:
                index = href.find('?') #removed shared match part of url
                href = href[0:index]
            if "/tests/" in href and href not in matches:
                matches.append(href)
        try:
            arrowButton = driver.find_element_by_xpath("//div[@class='matchesPagination']/div/a[2]")
            arrowButton.click()
            time.sleep(5)
            print "got matches for page " + str(i + 1)
            if i == 19:
                print "reached 20 pages of matches...did something go wrong?"
        except Exception as e:
            logDbg(e)
            break

    return matchName

def output(name, dict):
    global excluded
    global isToCsv
    global isToTxt

    if isToTxt:
        toTxt(name, dict)
    if isToCsv:
        toCsv(name, dict)

    if len(excluded) > 0:
        print "The following names were excluded:"
        for ex in excluded:
            print ex

def processGroup(driver, groupName, groupDict):
    print "Processing group: " + groupName
    dict={}
    matches = []
    primeMatchUrls = groupDict[groupName]
    for matchUrl in primeMatchUrls:
        matchName = processPrimeMatch(driver, dict, matches, matchUrl)

    for matchUrl in matches:
        processSharedMatch(driver, matchUrl, dict)
        logDbg(matchUrl)

    output(groupName, dict)

def main():
    global username
    global password
    global url
    global unkCounter

    groupArr = []
    groupDict = {}

    if len(sys.argv) > 1:
        infile = open(sys.argv[1], "r")
        for line in infile:
            columnsArr = line.split(",")
            matchName = columnsArr[0].decode('utf-8')
            groupName = columnsArr[1].decode('utf-8')
            exclude = columnsArr[2].decode('utf-8')
            matchUrl = columnsArr[3].decode('utf-8')
            if matchUrl.startswith("https") and groupName != '':
                 if groupName not in groupDict:
                     groupDict[groupName] = [matchUrl]
                     groupArr.append(groupName)
                 else:
                     groupDict[groupName] = groupDict[groupName] + [matchUrl]
            if exclude.lower() == 'y' or exclude.lower() == 'yes':
                exclusions.append(matchName)
        infile.close()

    if username == '':
        print "Email or Username:"
        username = raw_input()
    if password == '':
        password = getpass.getpass()
    if url == '' and len(groupArr) < 1:
        print "URL of match:"
        url = raw_input()
    else:
        firstGroup = groupArr[0]
        url = groupDict[firstGroup][0]

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(url)

    time.sleep(3)

    driver.switch_to.default_content()

    '''login'''
    iframe = driver.find_element_by_id('signInFrame')
    driver.switch_to_frame(iframe)

    element1 = driver.find_element_by_id(id_='username')
    pw = driver.find_element_by_id(id_='password')
    button = driver.find_element_by_id(id_='signInBtn')

    element1.send_keys(username)
    pw.send_keys(password)
    button.click()


    if len(groupArr) > 0:
        for group in groupArr:
            processGroup(driver, group, groupDict)
    else:
        dict={}
        matches = []
        matchName = processPrimeMatch(driver, dict, matches, '')

        for matchUrl in matches:
            processSharedMatch(driver, matchUrl, dict)
            logDbg(matchUrl)

        output(matchName, dict)

    driver.quit()

main()
