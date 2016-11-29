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
	
from bs4 import BeautifulSoup

from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import sqlite3
import webbrowser  


def addusertodatabase():
	########################################  ADD A USER TO DATABASE ################################# 
	##########   GET ACCOUNT   ##########   

	while True:
		try:
			print('Please enter your account name as it appears in the URL after "https://soundcloud.com/" ')
			accname = str(input('acc---> '))
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
			acczip = int(input('---> '))
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(acczip))
		except ValueError:
			print("Sorry, I didn't understand that. Please enter a valid zip code")
			continue
		else:
			break

	readyacczip = acczip

	# import json
	# with open('data.txt', 'w') as outfile:
	#     json.dump(data, outfile)


	##########   ADD TO DATABASE   ########## 

	accounts = {}

	accounts[readyacczip] = readyaccname

	with open('accounts.json', 'a') as fp:
		json.dump(accounts, fp, indent=4)

	print('Thank you, your account has been added as \"'+readyaccname+'\" (Full URL:', readyfullurl+")", 'with Zip Code', readyacczip)
	#options()

	# with open('accounts.json', 'w') as f:
	# 	json.dump([], f)

	options()



##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################

######### FIND A LIST OF USERS   ###########
def listofusers():
	while True:
		try:
			print('Please enter the zip code you would like to find accounts around')
			searchzip = int(input('---> '))
			print('Please enter the radius you would like to find accounts with')
			searchradius = int(input('---> '))
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(searchzip))
			#print(zipcode)
			mylat = re.findall('"Latitude": (\S+),', str(zipcode))
			mylong = re.findall('"Longitude": (\S+),', str(zipcode))
			# print('mylat-----',mylat)
			# print('mylong------',mylong)
			# print('LATITUDE====', zipcode.Latitude)
			# print('LONGITUDE====', zipcode.Longitude)
			# print('CITY=====', zipcode.City)
			res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius= searchradius, returns=100)
			#print('RES----------',len(res))
			len(res)
			searchresults = []
			for zipcode in res:
				searchresults.append(zipcode.Zipcode)
				#print('Zipcode: ',zipcode.Zipcode, '\n-->City: ', zipcode.City)
				searchcity = zipcode.City
				searchstate = zipcode.State 
		except ValueError:
			print("Sorry, I didn't understand that.")
			continue
		else:
			break
		#print('RESULTS -----', searchresults)

	############################################################
	############################################################
	with open('accounts.json', 'r') as fp:
	# accounts = json.load(fp)
		names = []
		zips = searchresults

		for acczip in fp:
			for zipcode in zips:
				#print(zipcode)
				x = '"'
				zipsearch = str(zipcode)
				y = '": "(\S+)"'
				myzipsearch = str(x + zipsearch + y)
				links = re.findall(myzipsearch, acczip)
				for link in links:
					names.append(link)
	print('\nSoundcloud users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + '):')
	for account in names:
		print(account)
	#print('NAMES----> ',names)
	print('\nPlease enter a number based on the following options:')
	print('1 - Open each of these user\'s profile')
	print('2 - Redo your search')
	print('3 - Return to the main menu')
	print('4 - Exit')
	option = input('---> ')
	if option == "1":
		for account in names:
			webbrowser.open('https://soundcloud.com/'+str(account), new=2, autoraise=True)
		options()
	elif option == "2":
		listofusers()
	elif option == "3":
		options()
	elif option == "4":
		exit()
	else:
		print('Sorry this was not a valid input')

def parseSoundcloud(x):


	chromedriver = "files/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)

	url = 'https://soundcloud.com/'+str(x)+'/tracks'
	driver.get(url)


	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")


	count = 0
	songlinks=[]
	elem = driver.find_element_by_tag_name('a')
	for x in range(500):
		try:
			elem.send_keys(Keys.PAGE_DOWN)
		except:
			print("error 1")
	#for x in driver.find_elements_by_class_name('sc-link-dark'):
	for x in driver.find_elements_by_class_name('soundTitle__title'):

		songlinks.append(x.get_attribute('href'))
		count += 1
	
	# myregx = 'https://soundcloud.com/'+str(x)
	# myregex = str('^' + myregx)
	# for item in songlinks:
	# 	# if not re.search(('^https://soundcloud.com/'+str(x)), item):
	# 	# 	songlinks.remove(item)

	# 	if not re.search(myregex, item):
	# 		songlinks.remove(item)



	# for item in songlinks:
	# 	print(item)
	# print(count)


	return songlinks
	driver.quit()

	# ###############
	# 	print(random.choice(songlinks))
	# 	another = input('To print another song enter \"y\" (or enter anything else to exit)\nEnter command---------------------->')	


	# 	while another == "y":
	# 		print(random.choice(songlinks))
	# 		another = input('To print another song enter \"y\" (or enter anything else to exit)\nEnter command---------------------->')
	# 	else:
	# 		print('Done')
	# 		exit()
	# 		driver.quit()


def getrandomsongs():
	artists = ['nickstevensent', 'ezequiel-rueda', 'maggierogers']
	templist = []
	totallist = []
	for item in artists:
		templist = parseSoundcloud(item)

		myregx = 'https://soundcloud.com/'+str(item)
		myregex = str('^' + myregx)
		#print('MY REGEX------ \n',myregex)
		for link in templist:
			# if not re.search(('^https://soundcloud.com/'+str(x)), item):
			# 	songlinks.remove(item)
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################

			if not re.search(myregex, link):
				templist.remove(link)


		totallist = totallist + templist

	# for item in totallist:
	# 	print(item)


	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################
	##########################################################################################################################################################################################


	###############
	print(random.choice(totallist))
	another = input('To print another song enter \"y\" (or enter anything else to exit)\nEnter command---------------------->')	


	while another == "y":
		print(random.choice(totallist))
		another = input('To print another song enter \"y\" (or enter anything else to exit)\nEnter command---------------------->')
	else:
		print('Done')
		exit()
	##################

	##########################################################################################################################################################################################
	##########################################################################################################################################################################################



	# #def moresongs():
	# another = input('To print another song enter \"y\"-->\n Or enter anything else to exit')
	# #while True:
	# while another == "y":
	# 	print('test')
	# 	another = input('To print another song enter \"y\"-->\n Or enter anything else to exit')
	# else:
	# 	print('done')
	# 	exit()
	# ######


def exit():
	print('Thank you for using LocalBeats. Have a good day!')



########## OPTIONS #############
def options():
	print('\nPlease enter a number based on the following options:')
	print('1 - Add a user to the database')
	print('2 - Find a list of users within a particular radius of a zip code')
	print('3 - Generate a random song link from users within a particular radius of a zip code')
	print('4 - Exit')



	#try:
	option = input('---> ')
	if option == "1":
		addusertodatabase()
	elif option == "2":
		listofusers()
	elif option == "3":
		getrandomsongs()
	elif option == "4":
		exit()
	else:
		print('Sorry this was not a valid input')
		#options()

	#except:
	#	print('Sorry this was not a valid input')
		#options()







options()

