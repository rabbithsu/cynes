# -*- coding: utf-8 -*- 

from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys 

from bs4 import BeautifulSoup
from datetime import *
import datetime
import time 
import os , sys
import urllib, urllib2
import codecs

start = date(2013, 01, 01)
end = datetime.date.today()
day = timedelta(1)
now = end

while(now != start):
	fn = os.path.join(os.path.dirname(__file__), "downloads_url", now.strftime('%Y-%m-%d')+".txt")
	if not os.path.exists(os.path.join(os.path.dirname(__file__), "downloads_url")):
		print "Can't find \"downloads_url\" folder."
		sys.exit(1)
	if os.path.isfile(fn):
		now = now + day
		break
	now = now - day

if now == end:
	print "No need update."
	sys.exit(0)

browser = webdriver.Chrome('chromedriver') 
browser.implicitly_wait(20)
searchurl = "http://news.cnyes.com/rollnews/"

while(now != end):
	success = True
	browser.get(searchurl + now.isoformat() + ".htm")
	time.sleep(5)
	save = ""
	count = 0
	while True:
		try:
			links = browser.find_elements_by_xpath('//div[@id="listArea"]/ul/li/a')
			for url in links:
				save = save + url.get_attribute("href") +"\n"
				count += 1
			buttun = browser.find_element_by_xpath('//a[text()=" 下一頁 > "]')

			if None != buttun.get_attribute("onclick"):
				#time.sleep(1)
				buttun.click()
			else:
				break
		except:
			save += "Can't load page.\n"
			success = False
			break;

	fn = os.path.join(os.path.dirname(__file__), "downloads_url", now.isoformat() +".txt")
	f = codecs.open(fn, "w+", "utf-8")
	f.write(save)
	f.close()

	if success:
		print time.strftime('%Y-%m-%d %H:%M:%S') + ":  file "+ now.isoformat()+ " finished.   " + str(count) + " links added."
	elif count != 0:
		print time.strftime('%Y-%m-%d %H:%M:%S') + ":  file "+ now.isoformat()+ " finished.   " + str(count) + " links added."
	else:
		print time.strftime('%Y-%m-%d %H:%M:%S') + ":  file "+ now.isoformat()+ " failed.   " + str(count) + " links added.  Can't load page."
	now += day
	
browser.close()
	






