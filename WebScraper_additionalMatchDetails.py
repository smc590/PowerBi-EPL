from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import requests
import pandas as pd
import sys

seasonLinks =["https://fbref.com/en/comps/9/1526/schedule/2016-2017-Premier-League-Scores-and-Fixtures",
"https://fbref.com/en/comps/9/1631/schedule/2017-2018-Premier-League-Scores-and-Fixtures",
"https://fbref.com/en/comps/9/1889/schedule/2018-2019-Premier-League-Scores-and-Fixtures",
"https://fbref.com/en/comps/9/3232/schedule/2019-2020-Premier-League-Scores-and-Fixtures"]

#get the links for matches
matchLinks=[]

for link in seasonLinks:
    req = Request(link)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")

    for matchLink in soup.findAll('a'):
        if(str(matchLink.get('href')).startswith('/en/matches') and str(matchLink.get('href')).endswith('Premier-League')):
            if('https://fbref.com/'+str(matchLink.get('href')) in matchLinks):
                pass
            else:
                matchLinks.append('https://fbref.com/'+str(matchLink.get('href')))


#print(matchLinks)

matchDetails = []

for matchLink in matchLinks:
    req = Request(matchLink)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")

    managers = soup.find_all(class_ ='datapoint')
    text=str(managers)
    ##find home manager
    h = re.search('Manager</strong>: (.+?)</div>,', text)
    if h:
        homemanager = h.group(1)

    ###find away manager
    a = re.search('/a></div>, <div class="datapoint"><strong>Manager</strong>: (.+?)</div>,',text)
    if a:
        awaymanager = a.group(1)

    try:
        matchDetails.append(matchLink+", Home Manager: "+ homemanager + "\nAway Manager: " + awaymanager)
    except AttributeError:
        matchDetails.append(matchLink+" error ")

    print(matchLink)
    try:
        print("Home manger: "+homemanager)
    except UnicodeEncodeError:
        print("\nERROR")
    try:
        print("\nAway manager"+awaymanager)
    except UnicodeEncodeError:
        print("\nERROR")
    

    #url = requests.get(matchLink)
    #tables = pd.read_html(url.text)

    tables=pd.read_html(matchLink)
    homerows = len(tables[3].index)
    awayrows = len(tables[5].index)
    matchDetails.append("Home yellows: " +str(tables[3].iat[homerows-1,12]))
    matchDetails.append("Home reds: " +str(tables[3].iat[homerows-1,13]))
    matchDetails.append("Away yellows: " +str(tables[5].iat[awayrows-1,12]))
    matchDetails.append("Away reds: " +str(tables[5].iat[awayrows-1,13]))
    try:
        print("\nHome yellows: " +str(tables[3].iat[homerows-1,12]))
    except UnicodeEncodeError:
        print("\nERROR")
    try:
        print("\nHome reds: " +str(tables[3].iat[homerows-1,13]))
    except UnicodeEncodeError:
        print("\nERROR")
    try:
        print("\nAway yellows: " +str(tables[5].iat[awayrows-1,12]))
    except UnicodeEncodeError:
        print("\nERROR")
    try:
        print("\nAway reds: " +str(tables[5].iat[awayrows-1,13]))
    except UnicodeEncodeError:
        print("\nERROR")
    
    
df = pd.DataFrame(matchDetails)
df.to_csv('matchDetails.csv')


