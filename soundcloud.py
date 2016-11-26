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


#######
	zips = self.db.get_zipcodes_around_radius(zipcode, radius)
	self.assertTrue(zipcode in [zip.zip for zip in zips])
#########

    def test_radius(self):
        zips = self.db.get_zipcodes_around_radius('54115', 30)
        self.assertTrue('54304' in [zip.zip for zip in zips])


getReposts('jproeser')

getAccountFromUser()
getZipFromUser()
taddToDatabase()
findAccounts()





fout = open('accounts.txt','w') --- used initially to create my file


















# # class ZipCodeDatabase(object):
  
# #     def __init__(self, conn_manager=None):
# #         if conn_manager is None:
# #             conn_manager = ConnectionManager()
# #         self.conn_manager = conn_manager
  
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

#     **中文文档**

#     查询某一个Zipcode的具体信息。
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

# #zipcode()
# print('ehy')
# # from pyzipcode import ZipCodeDatabase
# # zcdb = ZipCodeDatabase()
# # [z.zip for z in zcdb.get_zipcodes_around_radius('54901', 10)]

# from uszipcode import ZipcodeSearchEngine
# search = ZipcodeSearchEngine()
# zipcode = search.by_zipcode("10001")
# print(zipcode)

# mylat = re.findall('"Latitude": (\S+),', str(zipcode))
# mylong = re.findall('"Longitude": (\S+),', str(zipcode))
# print(mylat)
# print(mylong)
# ###########################  LAT  #######  LONG  ##########
# #res = search.by_coordinate(39.122229, -77.133578, radius=30, returns=5)
# #res = search.by_coordinate(int(mylat), int(mylong), radius=30)
# res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius=4, returns=100)

# len(res)
# for zipcode in res:
# 	#"^name: (\w+)"
# 	#myzip = re.search('^"Zipcode":  "(\w+)")', str(zipcode))
# 	myzip = re.findall('Zipcode": "(\S+)"', str(zipcode))
# 	#myzip = re.findall("Zipcode":, str(zipcode))
# 	#print(myzip)
# 	#print(Zipcode)
# 	print(zipcode.Zipcode)



# import zipcode

# class Zip(object):
# 	"""The zip code object."""
# 	def __init__(self, zip_tuple):
# 		self.zip = zip_tuple[_ZIP_CODE]
# 		"""The 5 digit zip code"""
# 		self.zip_type = zip_tuple[_ZIP_CODE_TYPE]
# 		"""The type of zip code according to USPS: 'UNIQUE', 'PO BOX', or 'STANDARD'"""
# 		self.city = zip_tuple[_CITY]
# 		"""The primary city associated with the zip code according to USPS"""
# 		self.state = zip_tuple[_STATE]
# 		"""The state associated with the zip code according to USPS"""
# 		self._location_type = zip_tuple[_LOCATION_TYPE] 
# 		# This value will always be 'Primary'. Secondary and 'Not Acceptable' placenames have been removed.
# 		self.lat = zip_tuple[_LAT]
# 		"""The latitude associated with the zipcode according to the National Weather Service.  This can be empty when there is no NWS Data"""
# 		self.lon = zip_tuple[_LONG]
# 		"""The longitude associated with the zipcode according to the National Weather Service. This can be empty when there is no NWS Data"""
# 		self._xaxis = zip_tuple[_XAXIS]
# 		self._yaxis = zip_tuple[_YAXIS]
# 		self._zaxis = zip_tuple[_ZAXIS]
# 		self._world_region = zip_tuple[_WORLD_REGION]
# 		# This value will always be NA for North America
# 		self._country = zip_tuple[_WORLD_REGION]
# 		# This value will always be US for United States -- This includes Embassy's, Military Bases, and Territories
# 		self.location_text = zip_tuple[_LOCATION_TEXT]
# 		"""The city with its state or territory. Example:  'Cleveland, OH' or 'Anasco, PR'"""
# 		self.location = zip_tuple[_LOCATION]
# 		"""A string formatted as WORLD_REGION-COUNTRY-STATE-CITY. Example: 'NA-US-PR-ANASCO'"""
# 		self.decommisioned = zip_tuple[_DECOMMISIONED]
# 		"""A boolean value that reveals if a zipcode is still in use"""
# 		self.tax_returns_filed = zip_tuple[_TAX_RETURNS_FILED]
# 		"""Number of tax returns filed for the zip code in 2008 according to the IRS"""
# 		self.population = zip_tuple[_ESTIMATED_POPULATION]
# 		"""Estimated population in 2008 according to the IRS"""
# 		self.wages = zip_tuple[_TOTAL_WAGES]
# 		"""Total wages according in 2008 according to the IRS"""
# 		self._notes = zip_tuple[_NOTES]
# 		# Not empty when there is no NWS data.

# 	def __repr__(self):
# 		return ''.format(zip=self.zip)

# 	def to_dict(self):
# 		vars_self = vars(self)
# 		bad_key_list = [x for x in vars_self.keys() if x[0] == '_']
# 		for key in vars_self.keys():
# 			if key in bad_key_list:
# 				del vars_self[key]
# 		return vars_self


# def isequal(zipcode):
# 	"""Takes a zipcode and returns the matching zipcode object.  If it does not exist, None is returned"""
# 	_validate(zipcode)
# 	_cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE == ?', [str(zipcode)])
# 	row = _cur.fetchone()
# 	if row:
# 		return Zip(row)
# 	else:
# 		return None

# def isinradius(point, distance):
# 	"""Takes a tuple of (lat, lon) where lon and lat are floats, and a distance in miles. Returns a list of zipcodes near the point."""
# 	zips_in_radius = list()
	
# 	if not isinstance(point, tuple):
# 		raise TypeError('point should be a tuple of floats')
# 	for f in point:
# 		if not isinstance(f, float):
# 			raise TypeError('lat and lon must be of type float')

# 	dist_btwn_lat_deg = 69.172
# 	dist_btwn_lon_deg = math.cos(point[0]) * 69.172
# 	lat_degr_rad = float(distance)/dist_btwn_lat_deg
# 	lon_degr_rad = float(distance)/dist_btwn_lon_deg

# 	latmin = point[0] - lat_degr_rad
# 	latmax = point[0] + lat_degr_rad
# 	lonmin = point[1] - lon_degr_rad
# 	lonmax = point[1] + lon_degr_rad

# 	if latmin > latmax:
# 		latmin, latmax = latmax, latmin
# 	if lonmin > lonmax:
# 		lonmin, lonmax = lonmax, lonmin

# 	stmt = ('SELECT * FROM ZIPS WHERE LONG > {lonmin} AND LONG < {lonmax}\
# 	 AND LAT > {latmin} AND LAT < {latmax}')
# 	_cur.execute(stmt.format(lonmin=lonmin, lonmax=lonmax, latmin=latmin, latmax=latmax))
# 	results = _cur.fetchall()

# 	for row in results:
# 		if haversine(point, (row[_LAT], row[_LONG])) <= distance:
# 			zips_in_radius.append(Zip(row))
# 	return zips_in_radius




  ################################
import sqlite3 as db
import os
from haversine import haversine
import math

_db_filename = 'zipcode.db'
_directory = os.path.dirname(os.path.abspath(__file__))
_zipcodedb_location = os.path.join(_directory, _db_filename)
_conn = db.connect(_zipcodedb_location)


_cur = _conn.cursor()

# positions
_ZIP_CODE = 0
_ZIP_CODE_TYPE = 1
_CITY= 2
_STATE = 3
_LOCATION_TYPE = 4
_LAT = 5
_LONG = 6
_XAXIS = 7
_YAXIS = 8
_ZAXIS = 9
_WORLD_REGION = 10
_COUNTRY = 11
_LOCATION_TEXT = 12
_LOCATION = 13
_DECOMMISIONED = 14
_TAX_RETURNS_FILED = 15
_ESTIMATED_POPULATION = 16
_TOTAL_WAGES = 17
_NOTES = 18

class Zip(object):
	"""The zip code object."""
	def __init__(self, zip_tuple):
		self.zip = zip_tuple[_ZIP_CODE]
		"""The 5 digit zip code"""
		self.zip_type = zip_tuple[_ZIP_CODE_TYPE]
		"""The type of zip code according to USPS: 'UNIQUE', 'PO BOX', or 'STANDARD'"""
		self.city = zip_tuple[_CITY]
		"""The primary city associated with the zip code according to USPS"""
		self.state = zip_tuple[_STATE]
		"""The state associated with the zip code according to USPS"""
		self._location_type = zip_tuple[_LOCATION_TYPE] 
		# This value will always be 'Primary'. Secondary and 'Not Acceptable' placenames have been removed.
		self.lat = zip_tuple[_LAT]
		"""The latitude associated with the zipcode according to the National Weather Service.  This can be empty when there is no NWS Data"""
		self.lon = zip_tuple[_LONG]
		"""The longitude associated with the zipcode according to the National Weather Service. This can be empty when there is no NWS Data"""
		self._xaxis = zip_tuple[_XAXIS]
		self._yaxis = zip_tuple[_YAXIS]
		self._zaxis = zip_tuple[_ZAXIS]
		self._world_region = zip_tuple[_WORLD_REGION]
		# This value will always be NA for North America
		self._country = zip_tuple[_WORLD_REGION]
		# This value will always be US for United States -- This includes Embassy's, Military Bases, and Territories
		self.location_text = zip_tuple[_LOCATION_TEXT]
		"""The city with its state or territory. Example:  'Cleveland, OH' or 'Anasco, PR'"""
		self.location = zip_tuple[_LOCATION]
		"""A string formatted as WORLD_REGION-COUNTRY-STATE-CITY. Example: 'NA-US-PR-ANASCO'"""
		self.decommisioned = zip_tuple[_DECOMMISIONED]
		"""A boolean value that reveals if a zipcode is still in use"""
		self.tax_returns_filed = zip_tuple[_TAX_RETURNS_FILED]
		"""Number of tax returns filed for the zip code in 2008 according to the IRS"""
		self.population = zip_tuple[_ESTIMATED_POPULATION]
		"""Estimated population in 2008 according to the IRS"""
		self.wages = zip_tuple[_TOTAL_WAGES]
		"""Total wages according in 2008 according to the IRS"""
		self._notes = zip_tuple[_NOTES]
		# Not empty when there is no NWS data.

	def __repr__(self):
		return '<Zip: {zip}>'.format(zip=self.zip)

	def to_dict(self):
		vars_self = vars(self)
		bad_key_list = [x for x in vars_self.keys() if x[0] == '_']
		for key in vars_self.keys():
			if key in bad_key_list:
				del vars_self[key]
		return vars_self

def _make_zip_list(list_of_zip_tuples):
	zip_list = list()
	for zip_tuple in list_of_zip_tuples:
		z = Zip(zip_tuple)
		zip_list.append(z)
	return zip_list


def _validate(zipcode):
	if not isinstance(zipcode, str):
		raise TypeError('zipcode should be a string')
	int(zipcode) # This could throw an error if zip is not made of numbers
	return True

def islike(zipcode):
	"""Takes a partial zip code and returns a list of zipcode objects with matching prefixes."""
	_validate(zipcode)
	_cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE LIKE ?', ['{zipcode}%'.format(zipcode=str(zipcode))])
	return _make_zip_list(_cur.fetchall())

def isequal(zipcode):
	"""Takes a zipcode and returns the matching zipcode object.  If it does not exist, None is returned"""
	_validate(zipcode)
	_cur.execute('SELECT * FROM ZIPS WHERE ZIP_CODE == ?', [str(zipcode)])
	row = _cur.fetchone()
	if row:
		return Zip(row)
	else:
		return None

def isinradius(point, distance):
	"""Takes a tuple of (lat, lon) where lon and lat are floats, and a distance in miles. Returns a list of zipcodes near the point."""
	zips_in_radius = list()
	
	if not isinstance(point, tuple):
		raise TypeError('point should be a tuple of floats')
	for f in point:
		if not isinstance(f, float):
			raise TypeError('lat and lon must be of type float')

	dist_btwn_lat_deg = 69.172
	dist_btwn_lon_deg = math.cos(point[0]) * 69.172
	lat_degr_rad = float(distance)/dist_btwn_lat_deg
	lon_degr_rad = float(distance)/dist_btwn_lon_deg

	latmin = point[0] - lat_degr_rad
	latmax = point[0] + lat_degr_rad
	lonmin = point[1] - lon_degr_rad
	lonmax = point[1] + lon_degr_rad

	if latmin > latmax:
		latmin, latmax = latmax, latmin
	if lonmin > lonmax:
		lonmin, lonmax = lonmax, lonmin

	stmt = ('SELECT * FROM ZIPS WHERE LONG > {lonmin} AND LONG < {lonmax}\
	 AND LAT > {latmin} AND LAT < {latmax}')
	_cur.execute(stmt.format(lonmin=lonmin, lonmax=lonmax, latmin=latmin, latmax=latmax))
	results = _cur.fetchall()

	for row in results:
		if haversine(point, (row[_LAT], row[_LONG])) <= distance:
			zips_in_radius.append(Zip(row))
	return zips_in_radius














# # print(isequal('60093'))

# from pyzipcode import ZipCodeDatabase
# zcdb = ZipCodeDatabase()
# zipcode = zcdb[54115]
# zipcode.zip
# #u'54115'
# zipcode.city
# #u'De Pere'
# zipcode.state
# #u'WI'
# zipcode.longitude
# #-88.078959999999995
# zipcode.latitude
# #44.42042
# zipcode.timezone
# #-6


# #Search zip codes...

# from pyzipcode import ZipCodeDatabase
# zcdb = ZipCodeDatabase()
# len(zcdb.find_zip(city="Oshkosh"))
# #7


# #Get a list of zipcodes around a radius of a zipcode

# from pyzipcode import ZipCodeDatabase
# zcdb = ZipCodeDatabase()
# [z.zip for z in zcdb.get_zipcodes_around_radius('54901', 10)]
# #[u'54901', u'54902', u'54903', u'54904', u'54906', u'54927', u'54952', u'54956', u'54957', u'54979', u'54985']



