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
from uszipcode import ZipcodeSearchEngine



 

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

def addusertodatabase():
	########################################  ADD A USER TO DATABASE ################################# 
	##########   GET ACCOUNT   ##########   
	print('\nHello, welcome to LocalBeats. Before we begin, you must add your profile to our database.')

	while True:
		try:
			print('Please enter your account name as it appears in the URL after "https://soundcloud.com/" ')
			accname = str(input('acc--->'))
			url = str("https://soundcloud.com/" + accname)
			request = requests.get(url)
			if request.status_code == 200:
				#print(accname)
				break
			else:
				print('\nSorry, this was an invalid response, please try again. Souncloud URL names must only use numbers, lowercase letters, underscores or hyphens, and they must start with a letter or number. \nPlease try again. And make sure you are connected to the internet.') 
				continue
		except:
			print('\nSorry, this was an invalid response, please try again. Souncloud URL names must only use numbers, lowercase letters, underscores or hyphens, and they must start with a letter or number. \nPlease try again. And make sure you are connected to the internet.') 
			continue
		else:
			break

	readyaccname = accname
	readyfullurl = url 

	##########   GET ZIP CODE   ##########   
	print('Please enter the permanent zip code you would like to associate with your account')

	while True:
		try:
			acczip = int(input('--->'))
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(acczip))
		except ValueError:
			print("Sorry, I didn't understand that. Please enter a valid zip code")
			continue
		else:
			break

	readyacczip = acczip

	##########   ADD TO DATABASE   ##########   
	accounts = {}

	accounts[readyacczip] = readyaccname

	with open('accounts.json', 'a') as fp:
		json.dump(accounts, fp, indent=4)

	print('Thank you, your account has been added as \"'+readyaccname+'\" (Full URL:', readyfullurl+")", 'with Zip Code', readyacczip)
	options()




######### FIND A LIST OF USERS   ###########
def listofusers():
	with open('accounts.json', 'r') as fp:
	    accounts = json.load(fp)
	for acczip in accounts:
		if acczip >= 4:
			print(acczip)
	
			# enter zipcode 
			# enter radius
			# find zip codes in radius

print('fdsaf')
doc = open('accounts.json')
# print (accounts['60093'])

for accounts in doc:
	print (accounts[jproeser])
	print ('Name')
print('list of users')


def randomsongs():
	print('random songs')



def exit():
	print('Thank you for using LocalBeats. Have a good day!')



########## OPTIONS #############
def options():
	print('\nPlease enter a number based on the following options:')
	print('1 - Add another user to the database')
	print('2 - Find a list of users within a particular radius of a zip code')
	print('3 - Generate a random song link from users within a particular radius of a zip code')
	print('4 - Exit')



	#try:
	option = input('Number-->')
	if option == "1":
		addusertodatabase()
	elif option == "2":
		listofusers()
	elif option == "3":
		randomsongs()
	elif option == "4":
		exit()
	else:
		print('Sorry this was not a valid input')
		#options()

	#except:
	#	print('Sorry this was not a valid input')
		#options()


























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

def myzipcode():
	#zcdb = ZipCodeDatabase()
	#self.db = pyzipcode.ZipCodeDatabase()
	
	zipcode = str(input('Enter a zip code'))
	radius = int(input('Enter a mile radius'))
	#[z.zip for z in zcdb.get_zipcodes_around_radius(zipcode, radius)]
    #def test_radius(self):

	zips = get_zipcodes_around_radius(zipcode, radius)
	assertTrue(zipcode in [zip.zip for zip in zips])


#######
	zips = self.db.get_zipcodes_around_radius(zipcode, radius)
	self.assertTrue(zipcode in [zip.zip for zip in zips])
#########

#     def test_radius(self):
#         zips = self.db.get_zipcodes_around_radius('54115', 30)
#         self.assertTrue('54304' in [zip.zip for zip in zips])


# getReposts('jproeser')

# getAccountFromUser()
# getZipFromUser()
# taddToDatabase()
# findAccounts()


#fout = open('accounts.txt','w') --- used initially to create my file







################


# from uszipcode import ZipcodeSearchEngine






# ##GET ZIPCODE

def getzipcodes():
	while True:
		try:
			print('Please enter the permanent zip code you would like to associate with your account')
			acczip = int(input('--->'))
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(acczip))
			print(zipcode)

			mylat = re.findall('"Latitude": (\S+),', str(zipcode))
			mylong = re.findall('"Longitude": (\S+),', str(zipcode))
			print('mylat-----',mylat)
			print('mylong------',mylong)
			print('LATITUDE====', zipcode.Latitude)
			print('LONGITUDE====', zipcode.Longitude)
			print('CITY=====', zipcode.City)
			###########################  LAT  #######  LONG  ##########
			#res = search.by_coordinate(39.122229, -77.133578, radius=30, returns=5)
			#res = search.by_coordinate(int(mylat), int(mylong), radius=30)
			res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius=10, returns=100)
			print('RES----------',len(res))
			len(res)
			for zipcode in res:
				#"^name: (\w+)"
				#myzip = re.search('^"Zipcode":  "(\w+)")', str(zipcode))
				##myzip = re.findall('Zipcode": "(\S+)"', str(zipcode))
				#myzip = re.findall("Zipcode":, str(zipcode))
				#print(myzip)
				#print(Zipcode)
				print('Zipcode: ',zipcode.Zipcode, '\n-->City: ', zipcode.City)
		except ValueError:
			print("Sorry, I didn't understand that.")
			continue
		else:
			break



































#options()



















# class ZipCodeDatabase(object):
  
#     def __init__(self, conn_manager=None):
#         if conn_manager is None:
#             conn_manager = ConnectionManager()
#         self.conn_manager = conn_manager
  
# def get_zipcodes_around_radius(zip, radius):
# 	# self = input('self')
# 	# zip = input('zip')
# 	# radius = input('radius')
# 	zips = zip
# 	if zips is None:
# 		raise ZipNotFoundException("Could not find zip code you're searching by.")
# 	else:
# 		zip = zips[0]

# 	radius = float(radius)

# 	long_range = (zip.longitude-(radius/69.0), zip.longitude+(radius/69.0))
# 	lat_range = (zip.latitude-(radius/49.0), zip.latitude+(radius/49.0))

# 	return format_result(conn_manager.query(ZIP_RANGE_QUERY % (
# 		long_range[0], long_range[1],
# 		lat_range[0], lat_range[1]
# 	)))

# def __init__(self,
#              Zipcode=None,  # 5 digits string zipcode
#              ZipcodeType=None,  # Standard or Po Box
#              City=None,  # city full name
#              State=None,  # 2 letter short state name
#              Population=None,  # estimate population
#              # estimate population per square miles (on land only)
#              Density=None,
#              TotalWages=None,  # estimate annual total wage
#              # estimate average annual wage = TotalWages/Population
#              Wealthy=None,
#              HouseOfUnits=None,  # estimate number of house unit
#              LandArea=None,  # land area in square miles
#              WaterArea=None,  # marine area in square miles
#              Latitude=None,  # latitude
#              Longitude=None,  # longitude
#              NEBoundLatitude=None,  # north east bound latitude
#              NEBoundLongitude=None,  # north east bound longitude
#              SWBoundLatitude=None,  # south west bound latitude
#              SWBoungLongitude=None,  # south west bound longitude
#              *args,
#              **kwargs
#              ):
#     self.Zipcode = Zipcode
#     self.ZipcodeType = ZipcodeType
#     self.City = City
#     self.State = State
#     self.Population = Population
#     self.Density = Density
#     self.TotalWages = TotalWages
#     self.Wealthy = Wealthy
#     self.HouseOfUnits = HouseOfUnits
#     self.LandArea = LandArea
#     self.WaterArea = WaterArea
#     self.Latitude = Latitude
#     self.Longitude = Longitude
#     self.NEBoundLatitude = NEBoundLatitude
#     self.NEBoundLongitude = NEBoundLongitude
#     self.SWBoundLatitude = SWBoundLatitude
#     self.SWBoungLongitude = SWBoungLongitude
    
#     __keys__ = [
#         "Zipcode",
#         "ZipcodeType",
#         "City",
#         "State",
#         "Population",
#         "Density",
#         "TotalWages",
#         "Wealthy",
#         "HouseOfUnits",
#         "LandArea",
#         "WaterArea",
#         "Latitude",
#         "Longitude",
#         "NEBoundLatitude",
#         "NEBoundLongitude",
#         "SWBoundLatitude",
#         "SWBoungLongitude",
#     ]

# def by_zipcode(self, zipcode, standard_only=True):
#     """Search zipcode information.

#     :param zipcode: integer or string zipcode, no zero pad needed
#     :param standard_only: bool, default True, only returns standard 
#       type zipcode
#     """
#     # convert zipcode to 5 digits string
#     zipcode = ("%s" % zipcode).zfill(5)

#     # execute query
#     select_sql = "SELECT * FROM zipcode WHERE Zipcode = '%s'" % zipcode
#     select_sql = self._sql_modify_standard_only(select_sql, standard_only)

#     res = self.cursor.execute(select_sql).fetchall()
#     if len(res) == 1:
#         return Zipcode(**res[0])
#     elif len(res) == 0:
#         return Zipcode()
#     else:
#         raise Exception("by_zipcode can not return multiple zipcode!")

#zipcode()
# from pyzipcode import ZipCodeDatabase
# zcdb = ZipCodeDatabase()
# [z.zip for z in zcdb.get_zipcodes_around_radius('54901', 10)]


