# import os
# from selenium import webdriver

# chromedriver = "/usr/local/bin/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)
# driver.get("http://stackoverflow.com")
# driver.quit()

# /usr/local/bin/chromedriver 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests
import re
import nltk
import json
from pyzipcode import Pyzipcode as pz
import unittest
import pyzipcode
#from pyzipcode import ZipCodeDatabase


 

#  import os
# from selenium import webdriver

# chromedriver = "/Users/adam/Downloads/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)
# driver.get("http://stackoverflow.com")
# driver.quit()


# Load WebDriver and navigate to the page url.
# This will open a browser window.
def getReposts(x):
	#chromedriver = "/usr/local/bin/chromedriver"
	chromedriver = "files/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)


	#driver = webdriver.Chrome("/files/chromedriver")
	url = 'https://soundcloud.com/'+str(x)+'/tracks'
	driver.get(url)
	 
	track_aria=[]
	elem = driver.find_element_by_tag_name('a')
	#print (elem)
	for x in range(500):
		try:
			elem.send_keys(Keys.PAGE_DOWN)
		except:
			print("fuuuucckkk")
	for x in driver.find_elements_by_class_name('sound'):
		track_aria.append(x.get_attribute('aria-label'))
	#driver.quit()


	theTracks=[]
	for track in track_aria:
		sub = re.findall('(?<=\:)(.*?)(?=\,)'.strip(), track)
		try:
			theTracks.append(sub[0].strip())
		except:
			print ("this thing")
	artists = []
	for x in theTracks:
		art = x.split("by")
		try:
			artists.append(str(art[1]).strip())
		except:
			pass
	return artists




## URLs USE ONLY NUMBERS, LOWECASE LETTERS, UNDERSCORES OR HYPHENS... C
def getAccountFromUser():
	print('\nHello, welcome to LocalBeats. Before we begin, you must add your profile to our database.')
	print('Please enter your account name as it appears in the URL after "https://soundcloud.com/" ')
	accname = str(input('acc--->'))

	# while True:
	# 	try:
	# 		accname = str(input('--->'))
	# 		#if re.search('[^a-z0-9]',accname):
	# 		#	print('111')
	# 		#	#print("Sorry, this was an invalid response, please try again. Souncloud URL names must only use numbers, lowercase letters, underscores or hyphens, and they must start with a letter or number.")
	# 		#	continue
	# 		#if re.search('-_a-z0-9',accname):
	# 		#	exit
	# 		#if re.search('^([a-z0-9])([a-z0-9')
	# 		#if not re.search('[a-z0-0]',accname) or re.search('_',accname) or re.search('-',accname):
	# 		#if re.search('[a-z0-9\-\_]+',accname):
			

	# 		if not re.match('^[a-z0-9]+[a-z0-9]+',accname):

	# 			print('bad')
	# 			continue
	# 		else:
	# 			print('good')
	# 			#print("Sorry, this was an invalid response, please try again. Souncloud URL names must only use numbers, lowercase letters, underscores or hyphens, and they must start with a letter or number.")
	# 			continue

	# 	except ValueError:
	# 		print("Sorry, this was an invalid response, please try again. Souncloud URL names must only use numbers, lowercase letters, underscores or hyphens, and they must start with a letter or number.")
	# 		#better try again... Return to the start of the loop
	# 		continue
	# 	else:
	# 		#age was successfully parsed!
	# 		#we're ready to exit the loop.
	# 		break
def getZipFromUser():
	print('Please enter the permanent zip code you would like to associate with your account')
	acczip = int(input('--->'))
	# while True:
	# 	try:
	# 		# Note: Python 2.x users should use raw_input, the equivalent of 3.x's input
	# 		acczip = int(input('--->'))
	# 	except ValueError:
	# 		print("Sorry, this was an invalid response, please try again. Souncloud URL names must only use numbers, lowercase letters, underscores or hyphens, and they must start with a letter or number.")
	# 		#better try again... Return to the start of the loop
	# 		continue
	# 	else:
	# 		# successfully parsed!
	# 		#we're ready to exit the loop.
	# 		break


def addToDatabase():
	accounts = {}
	accname = str(input('acc--->'))
	acczip = int(input('zip--->'))
	accounts[accname] = acczip

	# fout = open('accounts.txt', 'a')
	# fout.write(accounts)



	# with open('accounts.json', 'a') as f:
	#     json.dump(accounts, f)

	# # elsewhere...

	# with open('accounts.json') as f:
	#     accounts = json.load(f)

# 	with open('accounts', mode='w', encoding='utf-8') as f:
# 	    json.dump([], f)


# 	with open('accounts', mode='w', encoding='utf-8') as feedsjson:
# 	   # accounts = 
# 		feeds.append(accounts)
# 		json.dump(feeds, feedsjson)


# a_dict = {'new_key': 'new_value'}

	# with open('accounts.json') as f:
	# 	data = json.load(f)

	# data.update(accounts)

	# with open('accounts.json', 'w') as f:
	# 	json.dump(data, f)

	with open('accounts.json', 'a') as fp:
		json.dump(accounts, fp, indent=4)


# mydict = {'a': 1, 'b': 2, 'c': 3}
# output = open('myfile.pkl', 'wb')
# pickle.dump(mydict, output)
# output.close()

	#accounts = accname
	#accounts[zip] = acczip
	# print(accounts)
	# fhand = open('accounts.txt')
	# accounts = {}


def findAccounts():
	with open('accounts.json', 'r') as fp:
	    accounts = json.load(fp)
	for acczip in accounts:
		if acczip >= 4:
			print(acczip)

def zipcode():
	#zcdb = ZipCodeDatabase()
	#self.db = pyzipcode.ZipCodeDatabase()
	
	zipcode = str(input('Enter a zip code'))
	radius = int(input('Enter a mile radius'))
	#[z.zip for z in zcdb.get_zipcodes_around_radius(zipcode, radius)]
    #def test_radius(self):

	zips = get_zipcodes_around_radius(zipcode, radius)
	assertTrue(zipcode in [zip.zip for zip in zips])


########
	# zips = self.db.get_zipcodes_around_radius(zipcode, radius)
	# self.assertTrue(zipcode in [zip.zip for zip in zips])
##########

    # def test_radius(self):
    #     zips = self.db.get_zipcodes_around_radius('54115', 30)
    #     self.assertTrue('54304' in [zip.zip for zip in zips])


#getReposts('jproeser')

# getAccountFromUser()
# getZipFromUser()
#taddToDatabase()
#findAccounts()
zipcode()




#fout = open('accounts.txt','w') --- used initially to create my file
























class ZipCodeDatabase(object):
  
    def __init__(self, conn_manager=None):
        if conn_manager is None:
            conn_manager = ConnectionManager()
        self.conn_manager = conn_manager
  
    def get_zipcodes_around_radius(self, zip, radius):
        zips = self.get(zip)
        if zips is None:
            raise ZipNotFoundException("Could not find zip code you're searching by.")
        else:
            zip = zips[0]
  
        radius = float(radius)
  
        long_range = (zip.longitude-(radius/69.0), zip.longitude+(radius/69.0))
        lat_range = (zip.latitude-(radius/49.0), zip.latitude+(radius/49.0))
  
        return format_result(self.conn_manager.query(ZIP_RANGE_QUERY % (
            long_range[0], long_range[1],
            lat_range[0], lat_range[1]
        )))
        

