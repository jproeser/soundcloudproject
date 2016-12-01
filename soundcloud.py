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

def getzip():
	#gets a valid zip code from the user
	while True:
		try:
			x = input('---> ')
			#takes in input
			float(x)
			#try and except to validate that it is a number
			if len(str(x)) != 5:
				print('\nPlease enter a 5-digit zip code\n')
				continue
				#validate that it is a 5-digit zip code
		except ValueError:
			print ("\nThis is not a number. Please try again.\n")
			continue
		else:
			return x
			break

def getradius():
	#gets a valid search radius from the user
	while True:
		try:
			y = input('---> ')
			#takes in input			
			float(y)
			#try and except to validate that it is a number
			if str(y) == '0':
				print('\nPlease enter a search radius larger than 0\n')
				continue
		except ValueError:
			print ("\nThis is not a number. Please try again.\n")
			continue
		else: 
			return y
			break

def addusertodatabase():
	##########   GET ACCOUNT   ##########   
	while True:
		try:
			print('Please enter your account name as it appears in the URL after "https://soundcloud.com/" ')
			accname = str(input('acc---> '))
			url = str("https://soundcloud.com/" + accname)
			request = requests.get(url)
			if request.status_code == 200:
				#makes sure that the soundcloud account name is real by checking the url link to see if it exists/opens
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
			acczip = int(getzip())
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(acczip))
		except ValueError:
			print("\nSorry, I didn't understand that. Please enter a valid zip code")
			continue
		else:
			break
	readyacczip = acczip

	##########   ADD TO DATABASE   ########## 
	accounts = {}
	accounts[readyacczip] = readyaccname
	with open('accounts.json', 'a') as fp:
		#opens the existing file, rather than creating a new one
		json.dump(accounts, fp, indent=4)
		#adds the individual account zip and name in an organized format
	print('\nThank you, your account has been added as \"'+readyaccname+'\" (Full URL:', readyfullurl+")", 'with Zip Code', readyacczip)
	options()

def listofusers():
	#########   PROMPT USER FOR ZIP CODE AND RADIUS FOR SEARCH   ###########
	while True:
		try:
			print('\nPlease enter the zip code you would like to find accounts around')		
			searchzip = int(getzip())
			print('\nPlease enter the radius you would like to find accounts with')
			searchradius = int(getradius())

			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(searchzip))
			#searches zip code module for a given zipcode
			mylat = re.findall('"Latitude": (\S+),', str(zipcode))
			mylong = re.findall('"Longitude": (\S+),', str(zipcode))
			#finds the latitude and lognitude of a given zip code to be able to search for other zips in the radius
			res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius= searchradius, returns=100)
			#finds up to 100 zips in a given radius
			searchresults = []
			for zipcode in res:
				searchresults.append(zipcode.Zipcode)
				#stores each of the zip codes in a list
				searchcity = zipcode.City
				searchstate = zipcode.State 
		except:
			#try and except to only take real zip codes that exist
			print("\nSorry, I didn't understand that. Please enter a valid 5-digit zip code.\n")
			continue
		else:
			break
	#########    FIND A LIST OF USERS WIHTHIN DATABASE   ###########
	with open('accounts.json', 'r') as fp:
		names = []
		zips = searchresults
		for acczip in fp:
			for zipcode in zips:
				x = '"'
				zipsearch = str(zipcode)
				y = '": "(\S+)"'
				myzipsearch = str(x + zipsearch + y)
				#allows for the regex search to continually change based on the current zip code that you using from going through the list of zip codes in radius
				links = re.findall(myzipsearch, acczip)
				for link in links:
					names.append(link)
					#stores each of the names found in the zip code from the accounts database
		if len(names) > 0:
			print('\nSoundcloud users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + '):')
			for account in names:
				print(account)
		else:
		######### NO RESULTS IN SEARCH  ###########
			print('\nSorry, but we do not have any users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + ')')
			print('\nPlease enter a number based on the following options:')
			print('1 - Search again')
			print('2 - Add a user')
			print('3 - Return to the main menu')
			print('4 - Exit')
			def selections1():
				option = input('---> ')
				if option == "1":
					listofusers()
				elif option == "2":
					addusertodatabase()
				elif option == "3":
					options()
				elif option == "4":
					thanks()
				else:
					print('\nSorry this was not a valid input. Try again.')
					selections1()
			selections1()

	######### WHAT TO DO NEXT, GIVEN RESULTS  ###########
	print('\nPlease enter a number based on the following options:')
	print('1 - Open each user\'s profile')
	print('2 - Redo your search')
	print('3 - Return to the main menu')
	print('4 - Exit')
	def selections2():
		option = input('---> ')
		if option == "1":
			if len(names) > 0:
				for account in names:
					webbrowser.open('https://soundcloud.com/'+str(account), new=2, autoraise=True)
				print('\nThank you, the user accounts have been opened in your default browser and you are now back to the main menu')
				options()
			else:
				print('\nSorry, but we do not have any users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + ')')
		elif option == "2":
			listofusers()
		elif option == "3":
			options()
		elif option == "4":
			thanks()
		else:
			print('\nSorry this was not a valid input. Try again')
			selections2()
	selections2()

def parseSoundcloud(x):
	z = str(x)
	# chromedriver = "files/chromedriver"
	# os.environ["webdriver.chrome.driver"] = chromedriver
	# driver = webdriver.Chrome(chromedriver)
	####Possibility of opening the window of each account that is searched through, rather than doing it through phantom
	driver = webdriver.PhantomJS()
	driver.set_window_size(1120, 550)
	url = 'https://soundcloud.com/'+str(x)+'/tracks'
	driver.get(url)
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	songlinks=[]

	scheight = .1
	while scheight < 9.9:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
		scheight += .01
	#scrolls through the entire webpage so that all the songs are found, not just the first 10

	elem = driver.find_element_by_tag_name('a')

	for x in driver.find_elements_by_class_name('soundTitle__title'):
	#finds the link to each song of each user
		songlinks.append(x.get_attribute('href'))
		#stores this in a list
	driver.quit()
	return songlinks

def getrandomsongs():
	while True:
		try:
			print('\nPlease enter the zip code you would like to find accounts around')		
			searchzip = int(getzip())
			print('\nPlease enter the radius you would like to find accounts with')
			searchradius = int(getradius())
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(searchzip))
			mylat = re.findall('"Latitude": (\S+),', str(zipcode))
			mylong = re.findall('"Longitude": (\S+),', str(zipcode))
			res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius= searchradius, returns=100)
			searchresults = []
			for zipcode in res:
				searchresults.append(zipcode.Zipcode)
				searchcity = zipcode.City
				searchstate = zipcode.State 
		except:
			print("\nSorry, I didn't understand that. Please enter a valid 5-digit zip code.\n")
			continue
		else:
			break

	with open('accounts.json', 'r') as fp:
		names = []
		zips = searchresults
		for acczip in fp:
			for zipcode in zips:
				x = '"'
				zipsearch = str(zipcode)
				y = '": "(\S+)"'
				myzipsearch = str(x + zipsearch + y)
				links = re.findall(myzipsearch, acczip)
				for link in links:
					names.append(link)
		if len(names) > 0:
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
				#makes sure that only songs from the users in our database are kept in the list, since the parser can sometimes grab other songs that aren't the user's
				for link in templist:
					if re.match(myregex, link):
						totallist.append(link)

			print('\nDone! Here is a random song from the ' + str(numberusers) + ' soundcloud users in our database that are within ' + str(searchradius) + ' miles of ' + str(searchcity) + ', ' + str(searchstate) + ' (' + str(searchzip) + '):\n')

			def randsong():
				rsong = random.choice(totallist)
				#generates a random song
				return (rsong)

			def selection():
				print('\nPlease enter a number based on the following options:')
				print('1 - Generate a new random song')
				print('2 - Play this song')
				print('3 - Return to the main menu')
				print('4 - Exit')
				rsong = randsong()
				option = input('---> ')
				if option == "1":
					print('You may continually generate a new song by clicking 1. \n(Or you can choose options 2 (play), 3 (main menu) or 4 (exit) at any point.)\n')
					while option == "1":
						idk = randsong()
						print(idk)
						xyz = str(idk)
						option = input('---> ')	
					if option == "2":
						webbrowser.open(xyz, new=2, autoraise=True)
						#opens in a new tab in the same window
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

def thanks():
	print('Thank you for using LocalBeats. Have a good day!')
	exit()

def options():
	print('\n______________________Main Menu______________________\nPlease enter a number based on the following options:')
	print('1 - Add a user to the database')
	print('2 - Find a list of users within a particular radius of a zip code')
	print('3 - Generate a random song link from users within a particular radius of a zip code')
	print('4 - Exit')

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
		print('\nSorry this was not a valid input')
		options()

print('\nHello, welcome to LocalBeats. Before we begin, please make sure you have a strong internet connection.')
print('Additionally, if you are a SoundCloud user and you are not yet in our database, please add yourself by entering "1"')
options()



def init_randomusers():
	chromedriver = "files/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	url = 'https://soundcloud.com/ben-romijn/following'
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
	elem = driver.find_element_by_tag_name('a')
	for user in soup.find_all(class_='userBadgeListItem__title'):
		getuser = re.findall('/(\S+)" title',str(user))
		for u in getuser:
			songlinks.append(u)
	y = songlinks
	y = [x for x in y if not x.startswith('pro')]
	print('\nUSERS----', y)
def init_randomzips():
	while True:
		try:
			print('Please enter the zip code you would like to find accounts around')
			searchzip = int(input('---> '))
			print('Please enter the radius you would like to find accounts with')
			searchradius = int(input('---> '))
			search = ZipcodeSearchEngine()
			zipcode = search.by_zipcode(str(searchzip))
			mylat = re.findall('"Latitude": (\S+),', str(zipcode))
			mylong = re.findall('"Longitude": (\S+),', str(zipcode))
			res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius= searchradius, returns=100)
			searchresults = []
			for zipcode in res:
				searchresults.append(zipcode.Zipcode)
				searchcity = zipcode.City
				searchstate = zipcode.State 
		except:
			print("Sorry, I didn't understand that.")
			continue
		else:
			break

	print(searchresults)
def init_addusertodatabase():
	##########   GET ACCOUNT   ##########  
	x = 0
	while x < 300:  
		while True:
			try:
				accname = random.choice(randomusers)
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
		while True:
			try:
				#acczip = random.choice(morezips)
				acczip = random.choice(randomzips)
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
		print('\nThank you, your account has been added as \"'+readyaccname+'\"', 'with Zip Code', readyacczip, '\n ')
		#options()
		x += 1
def hideinfo():
	randomzips = []
	z1 = ['60093', '60091', '60043', '60022', '60026', '60201', '60203', '60025', '60053', '60077', '60062', '60076', '60714', '60202', '60035', '60712', '60645', '60040', '60646', '60626', '60016', '60659', '60015', '60068', '60631', '60090', '60660', '60630', '60656', '60625', '60070', '60018', '60056', '60640', '60706', '60641', '60634', '60069', '60618', '60045', '60613', '60089', '60004', '60176', '60657', '60005', '60639', '60647', '60707', '60171', '60044', '60131', '60614', '60061', '60651', '60008', '60074', '60622', '60007', '60106', '60302', '60642', '60160', '60305', '60301', '60191', '60164', '60610', '60644', '60088', '60624', '60165', '60612', '60654', '60173', '60048', '60067', '60304', '60611', '60661', '60064', '60606', '60104', '60602', '60601', '60153', '60603', '60607', '60604', '60143', '60130', '60163', '60605', '60195', '60101', '60804', '60623', '60126', '60608', '60157']
	z2 = ['79936', '79935', '79907', '79925', '79915', '79908', '79906', '79905', '79927', '79916', '79903', '79930', '79901', '79928', '79902', '79924', '79904', '79849', '79836', '79912', '79934', '79911', '79922', '79835', '88063', '79932', '79938', '79821', '88008', '88072', '88081', '88044', '88048', '88047', '88011', '79839', '88005', '88002', '88001', '88021', '88007', '88012', '88310', '88330', '79847', '87937', '88347', '87940', '88354', '87941', '88344', '88317', '88337', '87936', '87933', '88030', '88314', '88352', '87930', '88042', '87931', '88340', '87901', '88250', '88339', '87942', '88345', '88034', '88346', '88220', '88312', '88336', '88041', '88324', '88049', '88348', '88341', '88043', '79854', '88023', '88338', '88343', '88022', '88210', '87939', '88253', '88061', '88301', '87943', '88256', '87832', '88232', '88351', '88230', '79734', '88045', '88316', '88020', '79718', '79772']
	z3 = ['90011', '90037', '90021', '90058', '90007', '90015', '90079', '90014', '90013', '90001', '90062', '90255', '90003', '90071', '90017', '90006', '90023', '90018', '90057', '90002', '90033', '90012', '90043', '90270', '90005', '90044', '90010', '90047', '90063', '90020', '90026', '90008', '90305', '90004', '90019', '90201', '90016', '90059', '90031', '90302', '90029', '90280', '90040', '90022', '90061', '90056', '90303', '90301', '90036', '90032', '90222', '90262', '90038', '90039', '91754', '90065', '90028', '90304', '90232', '90035', '90048', '90034', '90230', '90249', '90027', '90211', '91803', '90045', '91755', '90250', '90042', '90240', '90247', '91205', '90640', '90241', '90221', '90220', '90068', '91204', '90041', '90212', '90069', '91030', '90723', '90094', '90506', '91210', '90660', '90046', '90067', '91801', '90064', '90260', '90242', '91608', '90248', '91203', '90066', '91206']
	z4 = ['90650', '90670', '90242', '90703', '90706', '90701', '90241', '90604', '90638', '90240', '90606', '90605', '90715', '90713', '90623', '90723', '90716', '90660', '90602', '90712', '90621', '90603', '90620', '90805', '90808', '90280', '90201', '90262', '90221', '90630', '92833', '90631', '90040', '90807', '90640', '90601', '90720', '90822', '90815', '90270', '92801', '91745', '90222', '92835', '90755', '92804', '90680', '90220', '90022', '92845', '92832', '90255', '90806', '90059', '91755', '90804', '90002', '91733', '90814', '92841', '91754', '90001', '90023', '90810', '90058', '91770', '90740', '90746', '90813', '92831', '90061', '90803', '90063', '91746', '92802', '92805', '90003', '90745', '92683', '90831', '92844', '92840', '91744', '90247', '91748', '90011', '91803', '90021', '90033', '91801', '90044', '90248', '91731', '91732', '92655', '91776', '92843', '92821', '92870', '90502']
	x1 = ['36608', '36695', '36575', '36619', '36618', '36587', '36609', '36541', '36693', '39562', '36613', '36607', '36606', '36544', '36612', '36617', '39452', '36605', '36604', '36615', '36610', '36582', '36603', '36602', '36611', '36571', '36509', '36572', '36521', '39563', '36527', '39581', '36523', '36525', '39565', '39553', '39567', '36505', '36526', '36522', '36532', '39564', '36528', '36560', '36584', '36551', '36578', '36576', '39540', '39456', '39530', '39451', '39532', '36555', '36507', '36580', '36553', '39531', '39461', '36535', '36579', '36511', '39573', '39577', '36529', '36567', '39507', '39574', '36542', '36539', '36583', '36562', '39561', '39423', '39501', '39362', '39503', '39425', '36530', '32568', '36574', '36550', '36585', '36561', '36518', '39560', '39462', '36549', '32526', '36502', '39571', '32577', '39476', '36548', '32533', '32506', '32535', '32507', '36558', '36480']
	x2 = ['99504', '99577', '99505', '99507', '99508', '99506', '99516', '99501', '99513', '99518', '99503', '99515', '99517', '99502', '99540', '99654', '99567', '99605', '99645', '99631', '99572', '99688', '99672', '99611', '99664', '99610', '99669', '99686', '99676', '99568']
	x3 =['85015', '85013', '85017', '85012', '85019', '85014', '85031', '85021', '85006', '85016', '85003', '85004', '85007', '85051', '85020', '85009', '85301', '85302', '85008', '85033', '85035', '85029', '85034', '85028', '85303', '85304', '85043', '85018', '85253', '85023', '85040', '85041', '85022', '85053', '85306', '85037', '85305', '85345', '85042', '85032', '85251', '85381', '85281', '85257', '85254', '85392', '85050', '85250', '85027', '85353', '85351', '85308', '85258', '85307', '85282', '85382', '85363', '85024', '85310', '85283', '85323', '85340', '85260', '85045', '85335', '85044', '85284', '85048', '85201', '85054', '85202', '85309', '85083', '85256', '85373', '85210', '85395', '85375', '85203', '85085', '85226', '85224', '85379', '85259', '85204', '85339', '85233', '85255', '85213', '85355', '85338', '85266', '85388', '85225', '85268', '85383', '85205', '85234', '85086', '85286']
	x4=['71601', '72004', '71644', '71603', '72152', '72175', '71602', '71667', '72073', '72168', '71665', '71643', '72072', '72079', '72057', '72046', '72132', '71639', '72003', '72055', '71652', '71662', '72160', '72150', '71655', '72042', '71660', '72065', '71725', '72142', '71671', '71670', '72166', '72206', '71742', '72129', '72103', '72024', '72011', '72026', '71631', '72038', '71675', '72134', '72086', '72209', '72128', '72048', '72117', '72084', '72041', '72140', '72064', '72022', '72202', '71766', '72114', '72201', '71674', '72015', '72204', '71654', '72167', '72205', '72069', '72116', '72207', '72211', '72076', '72002', '72227', '72210', '72212', '71642', '71638', '72029', '71720', '72019', '72223', '72118', '72104', '72017', '71744', '72023', '71647', '72333', '71763', '72120', '72113', '38769', '38746', '72176', '72040', '72007', '38726', '71651', '72366', '71658', '72021', '72087']
	x5=['80013', '80015', '80017', '80014', '80018', '80012', '80016', '80111', '80247', '80231', '80011', '80112', '80237', '80045', '80010', '80230', '80224', '80222', '80246', '80137', '80019', '80220', '80138', '80238', '80121', '80209', '80113', '80210', '80207', '80124', '80239', '80206', '80130', '80122', '80218', '80126', '80203', '80205', '80223', '80264', '80290', '80110', '80134', '80293', '80120', '80294', '80202', '80216', '80022', '80236', '80219', '80204', '80108', '80129', '80211', '80249', '80123', '80640', '80221', '80128', '80214', '80235', '80212', '80229', '80226', '80227', '80232', '80125', '80030', '80260', '80215', '80233', '80002', '80003', '80033', '80109', '80031', '80228', '80116', '80234', '80004', '80601', '80241', '80127', '80102', '80602', '80603', '80107', '80005', '80465', '80021', '80401', '80104', '80020', '80023', '80136', '80007', '80117', '80642', '80103']
	x6=['06010', '06062', '06786', '06085', '06489', '06716', '06032', '06052', '06013', '06782', '06479', '06053', '06787', '06704', '06051', '06037', '06001', '06022', '06107', '06779', '06778', '06710', '06791', '06705', '06702', '06111', '06451', '06110', '06795', '06706', '06023', '06410', '06708', '06119', '06106', '06117', '06020', '06089', '06019', '06712', '06057', '06109', '06450', '06105', '06114', '06067', '06092', '06103', '06112', '06770', '06416', '06751', '06762', '06002', '06481', '06120', '06763', '06070', '06455', '06059', '06759', '06790', '06798', '06492', '06457', '06758', '06518', '06108', '06118', '06750', '06524', '06081', '06403', '06480', '06063', '06090', '06095', '06033', '06488', '06422', '06073', '06793', '06473', '06035', '06098', '06756', '06478', '06514', '06065', '06026', '06040', '06074', '06777', '06794', '06783', '06042', '06472', '06441', '06483', '06096']
	x7=['32043', '32259', '32003', '32092', '32068', '32177', '32656', '32140', '32073', '32223', '32065', '32258', '32244', '32212', '32257', '32095', '32222', '32033', '32131', '32217', '32666', '32084', '32256', '32081', '32091', '32210', '32221', '32058', '32207', '32148', '32205', '32234', '32204', '32216', '32044', '32694', '32082', '32202', '32631', '32224', '32189', '32145', '32254', '32187', '32080', '32086', '32220', '32206', '32211', '32246', '32209', '32250', '32208', '32277', '32193', '32063', '32083', '32640', '32266', '32225', '32181', '32609', '32233', '32219', '32622', '32040', '32218', '32227', '32641', '32009', '32137', '32134', '32226', '32112', '32110', '32139', '32653', '32601', '32603', '32054', '32605', '32164', '32608', '32113', '32190', '31562', '32011', '32607', '32087', '32615', '32667', '32034', '32606', '32061', '32617', '32136', '32097', '34488', '32025', '32686']
	x8=['46033', '46038', '46280', '46032', '46290', '46062', '46250', '46240', '46074', '46256', '46037', '46060', '46220', '46260', '46236', '46216', '46034', '46268', '46077', '46226', '46205', '46055', '46235', '46228', '46208', '46278', '46218', '46030', '46040', '46254', '46069', '46051', '46075', '46229', '46219', '46201', '46222', '46048', '46202', '46204', '46031', '46224', '46203', '46214', '46225', '46234', '46064', '46239', '46112', '46107', '46011', '46052', '46163', '46241', '46237', '46227', '46050', '46072', '46016', '46044', '46013', '46167', '46221', '46123', '46049', '46231', '46217', '46259', '46140', '46186', '46056', '46036', '46017', '46142', '46130', '46168', '46012', '46149', '46068', '46143', '46057', '46113', '46117', '46076', '47384', '46001', '46071', '46039', '46126', '46161', '46147', '46184', '46122', '47356', '46902', '46162', '46165', '47334', '46110', '46979']
	x9=['07006', '07021', '07044', '07068', '07004', '07009', '07058', '07052', '07042', '07424', '07043', '07039', '07512', '07936', '07035', '07028', '07034', '07013', '07054', '07003', '07050', '07470', '07440', '07045', '07017', '07082', '07502', '07012', '07110', '07079', '07109', '07503', '07981', '07505', '07522', '07018', '07501', '07932', '07011', '07107', '07513', '07444', '07106', '07055', '07104', '07014', '07078', '07040', '07046', '07524', '07041', '07504', '07005', '07514', '07508', '07103', '07031', '07088', '07070', '07927', '07057', '07026', '07407', '07940', '07111', '07102', '07108', '07071', '07075', '07029', '07457', '07506', '07112', '07901', '07442', '07410', '07663', '07032', '07834', '07073', '07644', '07081', '07950', '07405', '07452', '07604', '07205', '07928', '07935', '07662', '07608', '07105', '07083', '07072', '07417', '07607', '07094', '07033', '07481', '07974']
	x10=['10021', '10075', '10065', '10028', '10044', '10128', '10022', '10154', '10023', '10111', '10112', '10167', '10024', '10017', '10020', '10170', '10174', '11102', '10173', '10168', '10029', '10165', '11109', '10019', '11106', '10069', '10016', '10036', '11101', '10018', '10025', '10119', '10026', '10035', '10199', '10001', '10010', '11103', '11104', '11105', '10115', '07093', '11222', '10003', '10027', '10011', '10454', '10009', '10037', '07086', '10030', '11377', '11370', '10014', '07020', '07087', '10451', '10012', '07010', '10031', '07030', '10455', '11378', '10002', '07022', '11211', '10039', '07047', '11372', '10013', '11371', '10103', '10110', '10152', '10153', '10162', '10169', '10171', '10172', '10177', '10271', '10279', '10278', '11206', '10474', '11373', '11369', '10007', '10282', '07310', '10456', '10038', '11237', '10032', '10452', '07307', '10006', '11201', '07657', '11205']
	x11 = ['29485', '29420', '29456', '29418', '29483', '29404', '29406', '29470', '29472', '29414', '29410', '29445', '29426', '29405', '29407', '29435', '29437', '29403', '29461', '29492', '29474', '29449', '29455', '29401', '29469', '29464', '29412', '29487', '29466', '29482', '29448', '29434', '29477', '29446', '29450', '29436', '29438', '29451', '29488', '29059', '29431', '29429', '29048', '29471', '29468', '29479', '29163', '29481', '29475', '29018', '29945', '29432', '29940', '29453', '29142', '29148', '29920', '29929', '29564', '29907', '29082', '29133', '29941', '29056', '29590', '29458', '29047', '29916', '29944', '29102', '29906', '29935', '29912', '29081', '29510', '29030', '29902', '29115', '29911', '29038', '29003', '29039', '29924', '29556', '29125', '29936', '29827', '29001', '29118', '29440', '29909', '29926', '29934', '29843', '29135', '29042', '29111', '29849', '29518', '29918']
	x12 = ['48009', '48084', '48304', '48025', '48072', '48073', '48017', '48076', '48098', '48301', '48070', '48034', '48083', '48067', '48302', '48237', '48075', '48069', '48071', '48033', '48322', '48220', '48085', '48341', '48334', '48310', '48092', '48342', '48309', '48323', '48221', '48030', '48320', '48235', '48219', '48336', '48314', '48091', '48203', '48326', '48240', '48307', '48328', '48340', '48324', '48223', '48015', '48331', '48238', '48093', '48312', '48317', '48152', '48335', '48227', '48234', '48313', '48239', '48088', '48089', '48212', '48316', '48327', '48204', '48206', '48306', '48359', '48228', '48154', '48375', '48329', '48390', '48377', '48026', '48211', '48202', '48127', '48126', '48066', '48150', '48205', '48315', '48038', '48213', '48021', '48360', '48210', '48208', '48035', '48386', '48201', '48036', '48128', '48167', '48135', '48363', '48382', '48225', '48374', '48094']
	randomzips = z1 + z2 +z3 +z4 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12
	morezips = []
	morezips = x10 + x11 + x12

	randomusers = []
	a = ['connor-stremmel', 'ianisiah', 'haresquead', 'd-uc-1', 'sanholobeats', 'harrbor', 'longlivecarl', 'jamessussman', 'yogmoney', 'maggierogers', 'ezequiel-rueda', 'nickstevensent', 'tom-pickren', 'surfskrt', 'epitometruth', 'brad-zach-smith', 'bleeklino', 'cub-j', 'the-scholar-rapper', 'easydeep-588530704', 'madi-beats', 'bradgurwin', 'lewisjamesgrant', 'redbullsoundselect', 'lilbando', 'beatsbybu', 'campaigne', 'tear-soup', 'dudemadison', 'nutothelo', 'connorwood-1', 'i-am-rella', 'zottimusic', 'off-narcotics', 'neonpajamas', 'noroeste']
	b = ['travisblack412', 'tiffanygouche', 'junglepussy', 'i-d-online-1', 'cardazzle', 'lachardon', 'icorvious', 'joe-rinaldo-heffernan', 'matthewstone', '1inamilli0nan93l', 'fadetomind', 'hazhitz', 'shlohmo', 'teamdtunez', 'preachgold', 'beyonce', 'donchristian', 'messkid', 'trae-harris-1', 'slow-head', 'lauren-devine', 'misterthumbs', 'gobby-2', 'britneyspears', 'dismagazine', 'totalfreedom', 'hipposintanks', 'physical-therapy', 'arca1000000', 'mykkiblanco', 'brenmar', 'hdhdhd', 'marronery', 'ghe20g0th1kradio']
	c = ['cakedog', 'asportinglife', 'driftonslow', 'cashmerecat', 'vase-1', 'kaytranada', 'itsdecibels', '247esp', 'nmemagazine', 'sinden', 'canblaster', 'purity-ring', 'citinite', 'marcopassarani', 'azealia-banks', 'dillonfrancis', 'diplo', 'illjohnkim', 'm-funx-made-in-glitch', 'addisongroove', 'badnewsbrian', 'calamalka', 'nautiluss', 'koreless', 'jacquesgreene', 'dza', 'curtisvodka', 'topbillinmusic', 'kool-clap', 'holdboxflat', 'theblessings', 'pgrooves', 'tokimonsta', 'theglitchmob', 'mrbeatnick', 'apparat']
	d = ['hardfest', 'donaldbucks', 'phantoms', 'ekalimusic', 'troyboi', 'piercefulton', 'callmegrant', 'happycolors', 'wearebreakfast', 'julianjordan', 'jay-hardway', 'trillmatics', 'designerdrugs', 'motorikrecords', 'funkagenda', 'brodinskiofficial', 'jumpjumpdancedance', 'deejayshe', 'grum', 'visitor', 'aeroplane', 'krismenace', 'grvrbbrs', 'moullinex', 'chrislake', 'jayceeoh', 'botnek', 'robyn', 'dj-steve1der', 'jimmyedgar', 'jpaulgetto', 'sammybananas', 'curious-poses', 'eliescobar', 'sof-1', 'late-nite-tuff-guy']
	e = ['oniwaida', 'planned_obsolescence', 'kingjet', 'shay-lia', 'gravez', 'theglitchmob', 'joey-purp', 'jonbap', 'bedtimelullabies', 'hrmxny', 'cri-music', 'samariasmusic', 'liluzivert', 'salvathore', 'pomrad', 'rubyfrancis', 'fknights', 'onlygirlmusic', 'indigoldtunes', 'gemaine', 'bjthechicagokid', 'muramasamusic', 'alliemoves', 'illmindmag', 'swagglerock', 'hotelgarudamusic', 'gitaofficial', 'krane', 'young-art-records', 'gallant', 'ekalimusic', 'ekali-bootlegs', 'tre-samuels', 'movingcastle', 'blackm0nday', 'sangobeats']
	f = ['jorgenodegard', 'hoverbootsmusic', 'starfucker_usa', 'iamshakka', 'cmnwlthcollective', 'sightlow', 'gunkst', 'xandg', 'elysianrecords', 'officialmedasin', 'liltexas', 'toofutureshop', 'venessamichaels', 'sikdope', '248mgmt', 'bigbabydram', 'herobust', 'snavs', 'odesza', 'owslaradio', 'quixofficial', 'purowuanmusic', 'purowuanremixes', 'commandqmusic', 'vintageculturemusic', 'tynvn', 'tascione', 'baadboys', 'lilaaron911', 'soysauce_url', 'chris_bushnell', 'joshpan', 'cartercruise', 'breauxofficial', 'stoltenhoff', 'riotville-records']
	g = ['futurehousemusic', 'heroboard', 'roughplates', 'solberjum', 'wegoheldeep', 'paulloebmusic', 'dave-winnel', 'hypeddit', 'timismag', 'oliverheldens', 'fargo', 'iamtchami', 'ducksaucenyc', 'harleyknox', 'wearegalantis', 'dj_tigerlily', 'themvth', 'chardy', 'saymynameofficial', 'dae-mons', 'melbourne-beats', 'melbourne-bangers', 'melbourne_underground', 'edmtunestv', 'mr-fluff', 'nomdestrip', 'wearegta', 'kidsatthebar', 'saviosavio', 'the-bay', 'edm', 'edm_planet', 'housemusic', 'dimmakrecords', 'hotmouth', 'dukedumont']
	h = ['phantogram', 'nkljv', 'buurmanandbuurman', 'richeyprofond', 'djhausuttu', 'volac', 'rinsefm', 'perspektiv-imprint', 'macsack', 'freestylers', 'wazeandodyssey', 'tafkamp', 'ilario-alicante', 'bodyjack', 'montelshouse', 'rogueedits-1', 'alanfitzpatrick', 'dungeonmeat', 'music-is-love-records-mcr', 'a-paul', 'uvb', 'ben-klock', 'norman-nodge', 'damn-bardak', 'jeroensearch', 'repitch', 'truss', 'siwell', 'remco-beekwilder', 'cahootsrecords', 'invite-1', 'snatchrecords', 'sunilsharpe', 'catzndogz', 'verknipt-amsterdam', 'selfreflektion']
	i = ['resistohr', 'vlaysin', 'mab-lab', 'format-amsterdam', 'cleric', 'pablo-gho', 'kevin-knops', 'raoul-konan', 'yannick-pinckers', 'alanfitzpatrick', 'rezystor', 'noah-verhoeff', 'undercontrol-paris', 'franklankhuizen', 'grndpodcast', 'deformation_booleenne_d_b', 'chapeleiro', 'level32records', 'molekulpage', 'markedamsterdam', 'airodmusic', 'oposition', 'lucy', 'stroboscopicartefacts', 'kegffnayy', 'tsait', 'ravensigh', 'fever-ray', 'dj-koze-official', 'jochempaap', 'tresorberlin', 'ihatemodels', 'reaktorevents', 'xosar', 'sigha', 'sntsrecords']
	j = ['beau-loers', 'user-964698084', 'flangerdrummer', '615243', 'mikehumphries', 'strobetechno', 'welovetechnomexico', 'd2techno', 'nbrec', 'carl-cox', 'iippupu', 'user-809176089', 'jop-coenen', 'dj-vas', 'user-38200247', 'zomboy', 'killthenoise', 'assertivef', 'minttunes', 'exquisitepr', 'fresh2deathmusic', 'ttomusic', 'i970', 'sicktaste-house', 'rudelies', 'joshhtaylorr', 'extraterramusic', 'm-t-aka-meddik-toxidelic', 'soulwaxofficial', 'chrisgresswell', 'builditrecords', 'ariusofficial', 'ajnavision-records', 'drumwerk', 'lickitloud', 'deepanddishy']
	randomusers = a + b + c + d + e + f + g + h + i + j 
	#print(randomusers)
	#print(total)
	#init_addusertodatabase()

	init_addusertodatabase()