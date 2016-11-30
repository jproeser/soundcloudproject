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

	##########   ADD TO DATABASE   ########## 
	accounts = {}
	accounts[readyacczip] = readyaccname
	with open('accounts.json', 'a') as fp:
		json.dump(accounts, fp, indent=4)
	print('Thank you, your account has been added as \"'+readyaccname+'\" (Full URL:', readyfullurl+")", 'with Zip Code', readyacczip)
	options()

def listofusers():
	#########   PROMPT USER FOR ZIP CODE AND RADIUS FOR SEARCH   ###########
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
			len(res)
			searchresults = []
			for zipcode in res:
				searchresults.append(zipcode.Zipcode)
				searchcity = zipcode.City
				searchstate = zipcode.State 
		except:
			print("Sorry, I didn't understand that. Please enter a valid zip code and mile radius")
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
				links = re.findall(myzipsearch, acczip)
				for link in links:
					names.append(link)
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
			print('2 - Return to the main menu')
			print('3 - Exit')
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
				print('Sorry this was not a valid input')
	######### WHAT TO DO NEXT, GIVEN RESULTS  ###########
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
	# chromedriver = "files/chromedriver"
	# os.environ["webdriver.chrome.driver"] = chromedriver
	# driver = webdriver.Chrome(chromedriver)
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

	elem = driver.find_element_by_tag_name('a')

	for x in driver.find_elements_by_class_name('soundTitle__title'):
		songlinks.append(x.get_attribute('href'))
	driver.quit()
	return songlinks


def getrandomsongs():
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
				for link in templist:
					if re.match(myregex, link):
						totallist.append(link)

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
		print('Sorry this was not a valid input')
		options()


# print('\nHello, welcome to LocalBeats. Before we begin, please make sure you have a strong internet connection.')
# print('Additionally, if you are a SoundCloud user and you are not yet in our database, please add yourself by entering "1"')
# options()

# while True:
# 	try:
# 		print('Please enter the zip code you would like to find accounts around')
# 		searchzip = int(input('---> '))
# 		print('Please enter the radius you would like to find accounts with')
# 		searchradius = int(input('---> '))
# 		search = ZipcodeSearchEngine()
# 		zipcode = search.by_zipcode(str(searchzip))
# 		mylat = re.findall('"Latitude": (\S+),', str(zipcode))
# 		mylong = re.findall('"Longitude": (\S+),', str(zipcode))
# 		res = search.by_coordinate(zipcode.Latitude, zipcode.Longitude, radius= searchradius, returns=100)
# 		searchresults = []
# 		for zipcode in res:
# 			searchresults.append(zipcode.Zipcode)
# 			searchcity = zipcode.City
# 			searchstate = zipcode.State 
# 	except:
# 		print("Sorry, I didn't understand that.")
# 		continue
# 	else:
# 		break

# print(searchresults)

total = []

z1 = ['60093', '60091', '60043', '60022', '60026', '60201', '60203', '60025', '60053', '60077', '60062', '60076', '60714', '60202', '60035', '60712', '60645', '60040', '60646', '60626', '60016', '60659', '60015', '60068', '60631', '60090', '60660', '60630', '60656', '60625', '60070', '60018', '60056', '60640', '60706', '60641', '60634', '60069', '60618', '60045', '60613', '60089', '60004', '60176', '60657', '60005', '60639', '60647', '60707', '60171', '60044', '60131', '60614', '60061', '60651', '60008', '60074', '60622', '60007', '60106', '60302', '60642', '60160', '60305', '60301', '60191', '60164', '60610', '60644', '60088', '60624', '60165', '60612', '60654', '60173', '60048', '60067', '60304', '60611', '60661', '60064', '60606', '60104', '60602', '60601', '60153', '60603', '60607', '60604', '60143', '60130', '60163', '60605', '60195', '60101', '60804', '60623', '60126', '60608', '60157']
z2 = ['79936', '79935', '79907', '79925', '79915', '79908', '79906', '79905', '79927', '79916', '79903', '79930', '79901', '79928', '79902', '79924', '79904', '79849', '79836', '79912', '79934', '79911', '79922', '79835', '88063', '79932', '79938', '79821', '88008', '88072', '88081', '88044', '88048', '88047', '88011', '79839', '88005', '88002', '88001', '88021', '88007', '88012', '88310', '88330', '79847', '87937', '88347', '87940', '88354', '87941', '88344', '88317', '88337', '87936', '87933', '88030', '88314', '88352', '87930', '88042', '87931', '88340', '87901', '88250', '88339', '87942', '88345', '88034', '88346', '88220', '88312', '88336', '88041', '88324', '88049', '88348', '88341', '88043', '79854', '88023', '88338', '88343', '88022', '88210', '87939', '88253', '88061', '88301', '87943', '88256', '87832', '88232', '88351', '88230', '79734', '88045', '88316', '88020', '79718', '79772']
z3 = ['90011', '90037', '90021', '90058', '90007', '90015', '90079', '90014', '90013', '90001', '90062', '90255', '90003', '90071', '90017', '90006', '90023', '90018', '90057', '90002', '90033', '90012', '90043', '90270', '90005', '90044', '90010', '90047', '90063', '90020', '90026', '90008', '90305', '90004', '90019', '90201', '90016', '90059', '90031', '90302', '90029', '90280', '90040', '90022', '90061', '90056', '90303', '90301', '90036', '90032', '90222', '90262', '90038', '90039', '91754', '90065', '90028', '90304', '90232', '90035', '90048', '90034', '90230', '90249', '90027', '90211', '91803', '90045', '91755', '90250', '90042', '90240', '90247', '91205', '90640', '90241', '90221', '90220', '90068', '91204', '90041', '90212', '90069', '91030', '90723', '90094', '90506', '91210', '90660', '90046', '90067', '91801', '90064', '90260', '90242', '91608', '90248', '91203', '90066', '91206']
z4 = ['90650', '90670', '90242', '90703', '90706', '90701', '90241', '90604', '90638', '90240', '90606', '90605', '90715', '90713', '90623', '90723', '90716', '90660', '90602', '90712', '90621', '90603', '90620', '90805', '90808', '90280', '90201', '90262', '90221', '90630', '92833', '90631', '90040', '90807', '90640', '90601', '90720', '90822', '90815', '90270', '92801', '91745', '90222', '92835', '90755', '92804', '90680', '90220', '90022', '92845', '92832', '90255', '90806', '90059', '91755', '90804', '90002', '91733', '90814', '92841', '91754', '90001', '90023', '90810', '90058', '91770', '90740', '90746', '90813', '92831', '90061', '90803', '90063', '91746', '92802', '92805', '90003', '90745', '92683', '90831', '92844', '92840', '91744', '90247', '91748', '90011', '91803', '90021', '90033', '91801', '90044', '90248', '91731', '91732', '92655', '91776', '92843', '92821', '92870', '90502']
x1 = ['36608', '36695', '36575', '36619', '36618', '36587', '36609', '36541', '36693', '39562', '36613', '36607', '36606', '36544', '36612', '36617', '39452', '36605', '36604', '36615', '36610', '36582', '36603', '36602', '36611', '36571', '36509', '36572', '36521', '39563', '36527', '39581', '36523', '36525', '39565', '39553', '39567', '36505', '36526', '36522', '36532', '39564', '36528', '36560', '36584', '36551', '36578', '36576', '39540', '39456', '39530', '39451', '39532', '36555', '36507', '36580', '36553', '39531', '39461', '36535', '36579', '36511', '39573', '39577', '36529', '36567', '39507', '39574', '36542', '36539', '36583', '36562', '39561', '39423', '39501', '39362', '39503', '39425', '36530', '32568', '36574', '36550', '36585', '36561', '36518', '39560', '39462', '36549', '32526', '36502', '39571', '32577', '39476', '36548', '32533', '32506', '32535', '32507', '36558', '36480']
x2 = ['99504', '99577', '99505', '99507', '99508', '99506', '99516', '99501', '99513', '99518', '99503', '99515', '99517', '99502', '99540', '99654', '99567', '99605', '99645', '99631', '99572', '99688', '99672', '99611', '99664', '99610', '99669', '99686', '99676', '99568']
total = z1 + z2 +z3 +z4 + x1 + x2
#print(total)



def addmyusers():
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

	##########   ADD TO DATABASE   ########## 
	accounts = {}
	accounts[readyacczip] = readyaccname
	with open('accounts.json', 'a') as fp:
		json.dump(accounts, fp, indent=4)
	print('Thank you, your account has been added as \"'+readyaccname+'\" (Full URL:', readyfullurl+")", 'with Zip Code', readyacczip)
	options()

def addsoundcloud():
	chromedriver = "files/chromedriver"
	os.environ["webdriver.Chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	# driver = webdriver.PhantomJS()
	# driver.set_window_size(1120, 550)
	#url = 'https://soundcloud.com/phantomfeels/following'
	url = 'https://soundcloud.com/maizecollective/following'
	driver.get(url)
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	songlinks=[]

	# scheight = .1
	# while scheight < 9.9:
	# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
	# 	scheight += .01

	#elem = driver.find_element_by_tag_name('div')

	for x in driver.find_elements_by_class_name('userBadgeListItem__title'):
		elem = driver.find_element_by_tag_name('a')
		for y in elem:
			songlinks.append(y.get_attribute('href'))
	#driver.quit()
	print (songlinks)
	
	# for user in soup.find_all(class_='userBadgeListItem__title'):
	# 	# z = str(user)
	# 	# getuser = re.findall('/(\S+)"',z)
	# 	# songlinks.append(getuser)
	# 	tags = user('a')
	# 	for tag in tags:
	# 	#second for loop, since there are multiple instances of tag a in the class
	# 		x = tag.contents[0]
	# 		print(x)
	# print(songlinks)


#options()
addsoundcloud()
#3 =['85015', '85013', '85017', '85012', '85019', '85014', '85031', '85021', '85006', '85016', '85003', '85004', '85007', '85051', '85020', '85009', '85301', '85302', '85008', '85033', '85035', '85029', '85034', '85028', '85303', '85304', '85043', '85018', '85253', '85023', '85040', '85041', '85022', '85053', '85306', '85037', '85305', '85345', '85042', '85032', '85251', '85381', '85281', '85257', '85254', '85392', '85050', '85250', '85027', '85353', '85351', '85308', '85258', '85307', '85282', '85382', '85363', '85024', '85310', '85283', '85323', '85340', '85260', '85045', '85335', '85044', '85284', '85048', '85201', '85054', '85202', '85309', '85083', '85256', '85373', '85210', '85395', '85375', '85203', '85085', '85226', '85224', '85379', '85259', '85204', '85339', '85233', '85255', '85213', '85355', '85338', '85266', '85388', '85225', '85268', '85383', '85205', '85234', '85086', '85286']
#4=['71601', '72004', '71644', '71603', '72152', '72175', '71602', '71667', '72073', '72168', '71665', '71643', '72072', '72079', '72057', '72046', '72132', '71639', '72003', '72055', '71652', '71662', '72160', '72150', '71655', '72042', '71660', '72065', '71725', '72142', '71671', '71670', '72166', '72206', '71742', '72129', '72103', '72024', '72011', '72026', '71631', '72038', '71675', '72134', '72086', '72209', '72128', '72048', '72117', '72084', '72041', '72140', '72064', '72022', '72202', '71766', '72114', '72201', '71674', '72015', '72204', '71654', '72167', '72205', '72069', '72116', '72207', '72211', '72076', '72002', '72227', '72210', '72212', '71642', '71638', '72029', '71720', '72019', '72223', '72118', '72104', '72017', '71744', '72023', '71647', '72333', '71763', '72120', '72113', '38769', '38746', '72176', '72040', '72007', '38726', '71651', '72366', '71658', '72021', '72087']
#5=['80013', '80015', '80017', '80014', '80018', '80012', '80016', '80111', '80247', '80231', '80011', '80112', '80237', '80045', '80010', '80230', '80224', '80222', '80246', '80137', '80019', '80220', '80138', '80238', '80121', '80209', '80113', '80210', '80207', '80124', '80239', '80206', '80130', '80122', '80218', '80126', '80203', '80205', '80223', '80264', '80290', '80110', '80134', '80293', '80120', '80294', '80202', '80216', '80022', '80236', '80219', '80204', '80108', '80129', '80211', '80249', '80123', '80640', '80221', '80128', '80214', '80235', '80212', '80229', '80226', '80227', '80232', '80125', '80030', '80260', '80215', '80233', '80002', '80003', '80033', '80109', '80031', '80228', '80116', '80234', '80004', '80601', '80241', '80127', '80102', '80602', '80603', '80107', '80005', '80465', '80021', '80401', '80104', '80020', '80023', '80136', '80007', '80117', '80642', '80103']
#6=['06010', '06062', '06786', '06085', '06489', '06716', '06032', '06052', '06013', '06782', '06479', '06053', '06787', '06704', '06051', '06037', '06001', '06022', '06107', '06779', '06778', '06710', '06791', '06705', '06702', '06111', '06451', '06110', '06795', '06706', '06023', '06410', '06708', '06119', '06106', '06117', '06020', '06089', '06019', '06712', '06057', '06109', '06450', '06105', '06114', '06067', '06092', '06103', '06112', '06770', '06416', '06751', '06762', '06002', '06481', '06120', '06763', '06070', '06455', '06059', '06759', '06790', '06798', '06492', '06457', '06758', '06518', '06108', '06118', '06750', '06524', '06081', '06403', '06480', '06063', '06090', '06095', '06033', '06488', '06422', '06073', '06793', '06473', '06035', '06098', '06756', '06478', '06514', '06065', '06026', '06040', '06074', '06777', '06794', '06783', '06042', '06472', '06441', '06483', '06096']
#7=
#8=
#9=
#10=
#11=
#12=
#13=
#14=
#15=
#16=
#17=
#18=
#19=
#20=
#21=
#22=
#23=
#24=
#25=
#26=
#27=
#28=
#29=
#30=
#31=
#32=
#33=
#34=
#35=
#36=
#37=
#38=
#39=
#40=
#41=
#42=
#43=
#44=
#45=
#46=
#47=
#48=
#49=
#50=

