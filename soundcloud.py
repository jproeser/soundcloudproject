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
			acczip = int(input('zip---> '))
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
		except:
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
		#print(zips)
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
		if len(names) > 0:

			print('\nSoundcloud users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + '):')
			for account in names:
				print(account)
		else:
			print('\nSorry, but we do not have any users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + ')')
			print('\nPlease enter a number based on the following options:')
			print('1 - Search again')
			print('2 - Return to the main menu')
			print('3 - Exit')
			option = input('---> ')
			if option == "1":
				listofusers()
			elif option == "2":
				options()
			elif option == "3":
				thanks()
			else:
				print('Sorry this was not a valid input')
	print('\nPlease enter a number based on the following options:')
	print('1 - Open each user\'s profile')
	print('2 - Redo your search')
	print('3 - Return to the main menu')
	print('4 - Exit')
	option = input('---> ')
	if option == "1":
		if len(names) > 0:
			for account in names:
				webbrowser.open('https://soundcloud.com/'+str(account), new=2, autoraise=True)
			print('\nThank you, the user accounts have been opened in your default browser and you are now back to the main menu')
			options()
		else:
			print('Sorry, but we do not have any users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + ')')
	elif option == "2":
		listofusers()
	elif option == "3":
		options()
	elif option == "4":
		thanks()
	else:
		print('Sorry this was not a valid input')


def parseSoundcloud(x):
	z = str(x)
	######################################################################################

	# chromedriver = "files/chromedriver"
	# os.environ["webdriver.chrome.driver"] = chromedriver
	# driver = webdriver.Chrome(chromedriver)

	# phantomdriver = "files/webdriver.py"
	# os.environ["webdriver.PhantomJS.driver"] = phantomdriver	
	# driver = webdriver.PhantomJS(phantomdriver)
	

	driver = webdriver.PhantomJS()
	driver.set_window_size(1120, 550)


	url = 'https://soundcloud.com/'+str(x)+'/tracks'
	driver.get(url)


	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")


	count = 0
	songlinks=[]

	scheight = .1
	while scheight < 9.9:
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
	    scheight += .01

	elem = driver.find_element_by_tag_name('a')
#	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


	# for x in range(500):
	# 	try:
	# 		elem.send_keys(Keys.PAGE_DOWN)
	# 	except:
	# 		print("scrolling error 1")
	#for x in driver.find_elements_by_class_name('sc-link-dark'):

	for x in driver.find_elements_by_class_name('soundTitle__title'):
#######ORIG
		songlinks.append(x.get_attribute('href'))
		count += 1
	

	# ##########



	# 	myregx = 'https://soundcloud.com/'+str(z)
	# 	myregex = str('^' + str(myregx))
	# 	z = x.get_attribute('href')
	# 	if re.search(myregex, z):

	# 			#	if re.search(myregex, link):



	# 		songlinks.append(z)
	# 	count += 1
	# 	#########

	# 	# z = x.get_attribute('href')
	# 	# #if re.search(myregex, z):

	# 	# 		#	if re.search(myregex, link):



	# 	# songlinks.append(z)
	# 	# count += 1



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

	driver.quit()
	# display.stop()
	for song in songlinks:
		print('song---- ', song)
	print ('count---', count)
	return songlinks

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
			res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius= searchradius, returns=100)
			#len(res)
			searchresults = []
			for zipcode in res:
				searchresults.append(zipcode.Zipcode)
				#print('Zipcode: ',zipcode.Zipcode, '\n-->City: ', zipcode.City)
				searchcity = zipcode.City
				searchstate = zipcode.State 
		except:
			print("Sorry, I didn't understand that.")
			continue
		else:
			break
		#print('RESULTS -----', searchresults)

	############################################################
	with open('accounts.json', 'r') as fp:
	# accounts = json.load(fp)
		names = []
		zips = searchresults
		#print(zips)
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
		if len(names) > 0:
		############################################################################
			artists = names
			templist = []
			totallist = []
			finallist = []
			numberusers = int(len(artists))
			x = int(len(artists))
			print('Searching through the SoundCloud accounts of the ' + str(x) + ' users we found in our database. \nPlease note that this may take a few minutes...')
			for item in artists:
				print('...Number of users left to search through: ' + str(x))
				x -= 1
				templist = parseSoundcloud(item)

				myregx = 'https://soundcloud.com/'+str(item)
				myregex = str('^' + str(myregx))
				#print('MY REGEX------ \n',myregex)
				for link in templist:
					# if not re.search(('^https://soundcloud.com/'+str(x)), item):
					# 	songlinks.remove(item)
			########################################################################################

					# if re.match(myregex, link):
					# 	totallist.append(link)
					# finallist += totallist


					# if re.match(myregex, link):
					# 	totallist += templist

					if re.match(myregex, link):
						totallist.append(link)


						#totallist.append()
				# 		templist.remove(link)

				# totallist = totallist + templist

			# for item in totallist:
			# 	print(item)


			#############

			###############
			#print(totallist)
			for s in totallist:

				print('finallist =====', s)
			print('Done! Here is a random song from the ' + str(numberusers) + ' soundcloud users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + '):')
			


			def randsong():
				rsong = random.choice(totallist)
				return (rsong)

			def selection():
				print('\nPlease enter a number based on the following options:')
				print('1 - Generate a new random song')
				print('2 - Play this song')
				print('3 - Return to the main menu')
				print('4 - Exit')
				rsong = randsong()
				#abc = str(rsong)
				option = input('---> ')
				if option == "1":
					print('You may continually generate a new song by clicking 1. \n(Or you can choose options 2 (play), 3 (main menu) or 4 (exit) at any point.)')
					#print (rsong)
					while option == "1":
						#rsong = random.choice(totallist)
						idk = randsong()
						print(idk)
						xyz = str(idk)
						option = input('---> ')	
					if option == "2":
						webbrowser.open(xyz, new=2, autoraise=True)
						selection()
					elif option == "3":
						options()
					elif option == "4":
						thanks()
					else:
						print('Sorry this was not a valid input')
				elif option == "2":
					webbrowser.open(hjkl, new=2, autoraise=True)
					selection()
				elif option == "3":
					options()
				elif option == "4":
					thanks()
				else:
					print('Sorry this was not a valid input')
					selection()

			uiop = randsong()
			print(uiop)
			hjkl = str(uiop)
			selection()




			# randomsong = random.choice(totallist)
			# print(randomsong)



			# print('\nPlease enter a number based on the following options:')
			# print('1 - Play this song')
			# print('2 - Generate a new random song')
			# print('3 - Return to the main menu')
			# print('4 - Exit')
			# option = input('---> ')
			# if option == "1":
			# 	webbrowser.open(randomsong, new=2, autoraise=True)
			# elif option == "2":
			# 	print('You may continually generate a new song by clicking 2, or you can choose options 1, 3 or 4 at any point.')
			# 	print(random.choise(totallist))
			# 	while option == "2":
			# 		rsong = random.choice(totallist)
			# 		print(rsong)
			# 		option = input('---> ')
			# 	if option == "1":
			# 		webbrowser.open(rsong, new=2, autoraise=True)
			# 	elif option == "3":
			# 		options()
			# 	elif option == "4":
			# 		thanks()
			# 	else:
			# 		print('Sorry this was not a valid input')
			# elif option == "3":
			# 	options()
			# elif option == "4":
			# 	thanks()
			# else:
			# 	print('Sorry this was not a valid input')





			# # another = input('\nTo print another song enter \"y\" (or enter anything else to return to main menu)\nEnter command----------------------> ')	


			# # while another == "y":
			# # 	print(random.choice(totallist))
			# # 	another = input('To print another song enter \"y\" (or enter anything else to return to main menu)\nEnter command----------------------> ')
			# # else:
			# # 	print('Done')
			# # 	options()
			# # 	#thanks()














		else:
			print('\nSorry, but we do not have any users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + ')')
			print('\nPlease enter a number based on the following options:')
			print('1 - Search again')
			print('2 - Return to the main menu')
			print('3 - Exit')
			option = input('---> ')
			if option == "1":
				getrandomsongs()
			elif option == "2":
				options()
			elif option == "3":
				thanks()
			else:
				print('Sorry this was not a valid input')



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


def thanks():
	print('Thank you for using LocalBeats. Have a good day!')
	exit()




########## OPTIONS #############
def options():
	print('\n______________________Main Menu______________________\nPlease enter a number based on the following options:')
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
		thanks()
	else:
		print('Sorry this was not a valid input')
		#options()

	#except:
	#	print('Sorry this was not a valid input')
		#options()







options()




# x = ['https://soundcloud.com/yellathug/sqrt', 'https://soundcloud.com/yellathug/kill-yoself', 'https://soundcloud.com/yellathug/dawp', 'https://soundcloud.com/yellathug/mella-fella', 'https://soundcloud.com/yellathug/the-fall', 'https://soundcloud.com/yellathug/cynicism', 'https://soundcloud.com/yellathug/nah-mean-prod-lowkey', 'https://soundcloud.com/yellathug/pikachu-prod-raymxn', 'https://soundcloud.com/yellathug/badlands-inst', 'https://soundcloud.com/yellathug/how-we-fall-v1', 'https://soundcloud.com/yellathug/savior', 'https://soundcloud.com/yellathug/soule-teaser', 'https://soundcloud.com/yellathug/ive-got-2', 'https://soundcloud.com/yellathug/misery', 'https://soundcloud.com/yellathug/fu-instrumental', 'https://soundcloud.com/yellathug/madman', 'https://soundcloud.com/yellathug/the-demo', 'https://soundcloud.com/yellathug/tattoo-prod-j-louis', 'https://soundcloud.com/yellathug/track-5', 'https://soundcloud.com/yellathug/3a-2', 'https://soundcloud.com/yellathug/2a-1', 'https://soundcloud.com/yellathug/tiobr-track-1']

# def randsong():
# 	rsong = random.choice(x)
# 	return (rsong)

# def selection():
# 	print('\nPlease enter a number based on the following options:')
# 	print('1 - Generate a new random song')
# 	print('2 - Play this song')
# 	print('3 - Return to the main menu')
# 	print('4 - Exit')
# 	rsong = randsong()
# 	#abc = str(rsong)
# 	option = input('---> ')
# 	if option == "1":
# 		print('You may continually generate a new song by clicking 1, or you can choose options 2 (play), 3 (main menu) or 4 (exit) at any point.')
# 		#print (rsong)
# 		while option == "1":
# 			#rsong = random.choice(totallist)
# 			idk = randsong()
# 			print(idk)
# 			xyz = str(idk)
# 			option = input('---> ')	
# 		if option == "2":
# 			webbrowser.open(xyz, new=2, autoraise=True)
# 			selection()
# 		elif option == "3":
# 			options()
# 		elif option == "4":
# 			thanks()
# 		else:
# 			print('Sorry this was not a valid input')
# 	elif option == "2":
# 		webbrowser.open(hjkl, new=2, autoraise=True)
# 		selection()
# 	elif option == "3":
# 		options()
# 	elif option == "4":
# 		thanks()
# 	else:
# 		print('Sorry this was not a valid input')
# 		selection()

# uiop = randsong()
# print(uiop)
# hjkl = str(uiop)
# selection()

























# 	if option == "1":
# 		webbrowser.open(rsong, new=2, autoraise=True)

# 		selection()
# 	elif option == "2":
# 		print('You may continually generate a new song by clicking 2, or you can choose options 1, 3 or 4 at any point.')
# 		#print(random.choice(totallist))
# 		while option == "2":
# 			#rsong = random.choice(totallist)
# 			randsong()
# 			option = input('---> ')
# 		if option == "1":
# 			webbrowser.open(rsong, new=2, autoraise=True)
# 		elif option == "3":
# 			options()
# 		elif option == "4":
# 			thanks()
# 		else:
# 			print('Sorry this was not a valid input')
# 	elif option == "3":
# 		options()
# 	elif option == "4":
# 		thanks()
# 	else:
# 		print('Sorry this was not a valid input')
# print(randsong())
