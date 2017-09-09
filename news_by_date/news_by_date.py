#encoding: utf-8
#2015-09 HSU
import urllib, urllib2
from bs4 import BeautifulSoup
from datetime import *
import time 
import codecs
import sys
import os
import re

day = timedelta(1)

if len(sys.argv) != 3:
    print "Input error."
    sys.exit(0)

else:
    if not re.search("\d\d\d\d/\d\d/\d\d", sys.argv[1]):
        print "Input error."
        sys.exit(0)
    elif not re.search("\d\d\d\d/\d\d/\d\d", sys.argv[2]):
        print "Input error."
        sys.exit(0)
    else:
        try:
            sdate = time.strptime(sys.argv[1], "%Y/%m/%d")
            edate = time.strptime(sys.argv[2], "%Y/%m/%d")
        except:
            print "Input error."
            sys.exit(0)
        start = date(sdate[0], sdate[1], sdate[2])
        end = date(edate[0], edate[1], edate[2])
        if end < start:
            print "Input error."
            sys.exit(0)
        now = start

print "Get news from " + start.strftime("%Y-%m-%d") + " to " + end.strftime("%Y-%m-%d")+"."

while(now != end+day):
    try:
        fn = os.path.join(os.path.dirname(__file__), "downloads_url", now.strftime("%Y-%m-%d")+".txt")
        fr = codecs.open(fn, "r", "utf-8" )
    except:
        print "Out of searching range."
        break
    for line in fr.readlines():
        if line == "Can't load page.\n":
            print "Can't load page.\n"
            continue
        save = ""
        soup = []
        url = line.replace("\n", "")
        try:
            content = urllib2.urlopen((url))
        except:
            print "Can't open url: " + url 
            continue
        soup = BeautifulSoup(content, 'html.parser')
		#set inside title
        try:
            save = soup.h1.string + "\n"
        except:
            print "Can't load news: " + url
            continue
        try:
            save += soup.find(class_="info").text
            save += "\n\n"
            #find date and time
            match = soup.find(class_="info").text
            tdate = re.search("\d\d\d\d-\d\d-\d\d", match).group().replace("-", "")
            ttime = re.search("\d\d:\d\d", match).group()[0:5].replace(":", "")
            #get tail
            path = soup.find(class_="crumb cDGray").find_all('a')
            tail = path[len(path)-1].string

            #get year
            title = "["+tdate+ttime+ "][" + soup.h1.string +"]["+tail+"]"
            title = title.replace("?", u"？")
            title = title.replace("/", u"／")
            title = title.replace("*", u"＊")
            title = title.replace("\\", u"＼")

            print title
            #check dir
            if not os.path.exists(tdate[0:4]):
                os.makedirs(tdate[0:4]);

            #get content
            for dlink in soup.find_all("p", attrs={'class': None}):
                if not dlink.a:
                    if not dlink.string:
                        save += ""
                    else:
                        save = save + dlink.string
        except:
            print "Something wrong."
            continue
        try:
            #openfile
            fw = os.path.join(os.path.dirname(__file__), tdate[0:4],title+".txt")
            f = codecs.open(fw, "w+", "utf-8")
            #write file
            f.write(save)
            f.close()
            time.sleep(1)
        except:
            print "Write file " + title + "fails."
            continue
    fr.close()
    print now.strftime("%Y-%m-%d") + " finished."
    now += day
