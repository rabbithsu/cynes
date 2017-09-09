#encoding: utf-8
#2015-08-20 HSU
import re
import time
import os
import sys
import codecs
from time import strftime
from bs4 import BeautifulSoup
import urllib, urllib2

if len(sys.argv) < 2:
    print "Get today's news."
    findurl = "http://news.cnyes.com/Content/"+time.strftime("%Y%m%d") +"/"
else:
    if sys.argv[1] == "-a":
        print "Get all in list."
        findurl = "http://news.cnyes.com/Content/"
    else:
        print "Not difined comment.Get today's news."
        findurl = "http://news.cnyes.com/Content/"

end = False

for j in range(100):
    soup = []
    if j == 0:
        continue
    elif j == 1:
        url = urllib2.urlopen("http://news.cnyes.com/rollnews/list.shtml?ga=nav")
        soup = BeautifulSoup(url, 'html.parser')
    else:
        url = urllib2.urlopen("http://news.cnyes.com/rollnews/list_"+str(j)+".shtml")
        soup = BeautifulSoup(url, 'html.parser')
    if not soup:
        break

    for link in soup.find_all(href=re.compile(findurl)):
        data = urllib2.urlopen(link.get('href'))
        dsoup = BeautifulSoup(data, 'html.parser')
        save = dsoup.h1.string + "\n"
        save += dsoup.find(class_="info").string
        save += "\n\n"
        dtitle = link.get('href').split("/")[4]
        title = dtitle + dsoup.h1.string
        title = title.replace("?", u"？")
        title = title.replace("/", u"／")
        print title
        if not os.path.exists(dtitle[0:4]):
            os.makedirs(dtitle[0:4]);
        fn = os.path.join(os.path.dirname(__file__), dtitle[0:4], title+".txt")
        f = codecs.open(fn, "w+", "utf-8")
        for dlink in dsoup.find_all("p", attrs={'class': None}):
	   	   if not dlink.a:
			     if not dlink.string:
				    save += ""
			     else:
				    save = save + dlink.string
        f.write(save)
        f.close()
        time.sleep(1)
    if(end):
        break


