import requests
from bs4 import BeautifulSoup
import time
import os

import json

from pathlib import Path

import re 
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	driver.implicitly_wait(3)

	return driver


### Make JSON file with collected data ###
def json_output(profile):
	file_exists = os.path.isfile('voices.json')
	if not file_exists:
		data = {"profiles": []}
		with open("voices.json", "w+") as file:
			json.dump(data, file, indent=4)
		print(data)

	with open("voices.json", "r+") as file:
		data = json.load(file)
		data['profiles'].append(profile)

		json.dumps(data, indent=4)

	with open("voices.json", "w+") as file:
		json.dump(data, file, indent=4)

	print("Json data added. Going for next profile")
		




## for single demo audio data
def demo_audio(link):
	response 	= requests.get(link)
	time.sleep(0.5)
	soup 		= BeautifulSoup(response.text, features='html.parser')

	demo_title_span = soup.find('span', {'class': 'profile-demo-title'})
	demo_title 		= demo_title_span.find('h2')
	if demo_title:
		demo_title = demo_title.text

	listens = soup.find('span', {'class': 'profile-demo-listens'}).text.strip()

	demo_details 	= soup.find_all('div', {'class': 'profile-demo-detail'})
	i = 0
	catagorie = ""
	try:
		strong = demo_details[i].find('strong').text
		if strong == "Category":
			catagorie = demo_details[i].find('span').text.strip()
			i = i+1
	except:
		pass

	language = ""
	try:
		strong = demo_details[i].find('strong').text
		if strong == "Language":
			language = demo_details[i].find('span').text.strip()
			i = i+1
	except:
		pass


	voice_age = ""
	try:
		strong = demo_details[i].find('strong').text
		if strong == "Voice Age":
			voice_age = demo_details[i].find('span').text.strip()
			i = i+1
	except:
		pass

	description = ""
	try:
		strong = demo_details[i].find('strong').text
		if strong == "Description":
			description = demo_details[i].find('span').text.strip()
			i = i+1
	except:
		pass

	transcript = ""
	try:
		strong = demo_details[i].find('strong').text
		if strong == "Transcript":
			transcript = demo_details[i].find('span').text.strip()
			i = i+1
	except:
		pass

	tags = []
	try:
		strong = demo_details[i].find('strong').text
		if strong == "Tags":
			tag 	= demo_details[i].find('span')
			tag_a 	= tag.findAll('a')
			for a in tag_a:
				tags.append(a.text.strip())				
			i = i+1
	except:
		pass

	demo = {
		"Demo Name"		: demo_title,
		"Listens"		: listens,
		"Category"		: catagorie,
		"Language"  	: language,
		"Voice Age"		: voice_age,
		"Description"	: description,
		"Transcript"	: transcript,
		"Tags"			: tags

	}
	return demo


## demo audio list
def demo_audio_list(demo_url):
	print("Getting demo audio data..")
	time.sleep(1)
	response = requests.get(demo_url)
	soup 	= BeautifulSoup(response.text, features='html.parser')

	demo_audio_links = soup.find_all('a', {'class': 'profile-demo-link'})
	# print(demo_audio_links)
	all_demo = []
	for l in demo_audio_links:
		link = l.get('href')
		print(link)
		link = "https://www.voices.com" + link
		print(link)
		demo = demo_audio(link)
		all_demo.append(demo)
		time.sleep(1)
	return all_demo






## collect single profile data
def profile(profile_url):
	print("We are in profile page...")	
	response 	= requests.get(profile_url)
	time.sleep(3)
	soup 		= BeautifulSoup(response.text, features='html.parser')
	profile_info	= soup.find('div', {'class': 'profile-info'})
	actor_name 		= profile_info.find('h1').text
	actor_name 		= actor_name.strip()
	actor_address	= profile_info.find('p', {'class': 'public-address-and-timezone'})
	local_time 		= actor_address.find('strong').text
	actor_address 	= actor_address.text.split(local_time)[0].strip()

	try:
		stars_review 	= profile_info.find('div', {'class': 'stars-text'})
		stars 			= stars_review.find('span', {'class': 'text-grey1'}).text.strip()
		reviews 		= stars_review.find('a', {'class': 'link'}).text.strip()
	except:
		stars 			= "No job yet"
		reviews 		= "No reviews"


	profile_sideber = soup.find('div', {'id': 'profile-sidebar'})
	sidebar_boxs 	= profile_sideber.find_all('div', {'class':'profile-content-box'})

	actor_info 		= sidebar_boxs[0].find_all('div', {'class': 'profile-metadata'})
	# print(actor_info)
	replies_in = ""
	member_since = ""
	completed_jobs = ""
	i = 0
	try:
		h5 = actor_info[i].find('h3', {'class': 'h5'}).text
		if h5 == "Usually Replies in":
			replies_in = actor_info[i].find('p').text
			i = i+1

	except:
		pass

	try:
		h5 = actor_info[i].find('h3', {'class': 'h5'}).text
		if h5 == "Member Since":
			member_since = actor_info[i].find('p').text
			i = i+1
	except:
		pass


	try:
		h5 = actor_info[i].find('h3', {'class': 'h5'}).text
		if h5 == "Completed Jobs":
			completed_jobs = actor_info[i].find('p').text
			i = i+1
	except:
		pass

	voice_vocal_sections = sidebar_boxs[1].find_all('div', {'class': 'profile-content-section'})


	languages = []
	language = soup.find('p', {'id': 'profile-languages'})
	if language:
		lan = language.text.split(',')
		for l in lan:
			languages.append(l.strip())

	accents_list = []
	accents = soup.find('p', {'id': 'accents-list'})
	if accents:
		acce = accents.text.split(',')
		for a in acce:
			accents_list.append(a.strip())
	

	
	voice_agent = voice_vocal_sections[2].find('p', {'class': 'margBot0'})
	if voice_agent:
		voice_agent = voice_agent.text

	
	skill_catagories = soup.find('p',{'id': 'vocal-skills-categories'})
	if skill_catagories:
		skill_catagories = skill_catagories.text

	vocal_skill = {
		"Languageas" 	: languages,
		"Accents List"	: accents_list,
		"Voice Ages"	: voice_agent,
		"Catagories"	: skill_catagories,
	}

	studio_section = sidebar_boxs[2].find_all('div', {'class': 'profile-content-section'})

	i = 0
	turnaround_time = ""
	try:
		h5 = studio_section[i].find('h3', {'class': 'h5'}).text
		if "Turnaround Time" in h5:
			turnaround_time = studio_section[i].find('p',{'class': 'margBot0'}).text
			i = i+1
	except:
		pass

	live_directed_session = ""
	try:
		h5 = studio_section[i].find('h3', {'class': 'h5'}).text
		if "Live Directed Sessions" in h5:
			live_directed_session = studio_section[i].find('p',{'class': 'margBot0'}).text
			i = i+1
	except:
		pass


	microphone = ""
	try:
		h5 = studio_section[i].find('h3', {'class': 'h5'}).text
		if "Microphone" in h5:
			microphone = studio_section[i].find('p',{'class': 'margBot0'}).text
			i = i+1
	except:
		pass


	computer_software = ""
	try:
		h5 = studio_section[i].find('h3', {'class': 'h5'}).text
		if "Computer & Software" in h5:
			computer_software = studio_section[i].find('p',{'class': 'margBot0'}).text
			i = i+1
	except:
		pass


	spacial_equipment = ""
	try:
		h5 = studio_section[i].find('h3', {'class': 'h5'}).text
		if "Special Equipment" in h5:
			spacial_equipment = studio_section[i].find('p', {'class': 'margBot0'}).text
			i = i+1
	except:
		pass

	studio = {
		"Turnaround Time"		: turnaround_time,
		"Live Directed Sessions": live_directed_session,
		"Microphone"			: microphone,
		"Computer & Software"	: computer_software,
		"Special Equipment"		: spacial_equipment
	}
	# print(studio)
	


	# about_actor = soup.find('div', {'class': 'profile-content-section-bordered'})
	# print(about_actor)

	overview 	= soup.find('p', {'id': 'profile-overview'})
	if overview:
		overview = overview.text.strip()

	description = soup.find('p', {'id': 'profile-description'})
	if description:
		description = description.text


	experience = soup.find('p', {'id': 'profile-clients'})
	if experience:
		experience = experience.text

	list_of_clients = []
	client_list = soup.find('p', {'id': 'profile-experience'})
	if client_list:
		client_list = client_list.text
		client_list = client_list.split(',')
		for client in client_list:
			list_of_clients.append(client.strip())

	education = ""
	education = soup.find('p', {'id': 'profile-education'})
	if education:
		education = education.text


	all_testimonial = []
	testimonial_div = soup.find('div', {'id': 'profile-testimonials'})
	if testimonial_div:
		testimonials 	= testimonial_div.findAll('blockquote')
		for i in range(len(testimonials)):
			testimonial_peragraph 	= testimonials[i].find('p').text
			testimonial_by 			= testimonials[i].find('small').text

			testimonial	= {
				"testimonial": testimonial_peragraph,
				"testimonial_by": testimonial_by
				}
			all_testimonial.append(testimonial)

	more_information_div = soup.find('div', {'id': 'profile-more-info'})

	all_queation_answer = []
	if more_information_div:
		information_divs = more_information_div.find_all('div', {'class': 'profile-content-section'})
		for i in range(len(information_divs)):
			queation 	= information_divs[i].find('h3', {'class': 'h5'}).text
			answer 		= []
			li 			= information_divs[i].find_all('li')
			for l in range(len(li)):
				ans = li[l].text.strip()
				ans = "{}. ".format(l+1) + ans
				answer.append(ans)
			queation_answer = {
				"Queation"	: queation,
				"Answer"	: answer
			}
			all_queation_answer.append(queation_answer)


	demo_url = profile_url+"/demos"
	print(demo_url)
	all_demo = demo_audio_list(demo_url)



	profile = {
		"Actor name" 		: actor_name,
		"Actor address"		: actor_address,
		"Local time"		: local_time,
		"Stars" 			: stars,
		"Reviews"			: reviews,
		"Usually Replies In": replies_in,
		"Member Since"		: member_since,
		"Completed Jobs"	: completed_jobs,
		"Vocal Skill"		: vocal_skill,
		"Studio" 			: studio,
		"Overview" 			: overview,
		"Description"		: description,
		"Experience"		: experience,
		"List of clients"	: list_of_clients,
		"All Testimonial"	: all_testimonial,
		"Queation & Answer" : all_queation_answer,
		"Demos"				: all_demo
	}

	json_output(profile)
	return None
	
## login voices.com
def login(driver):
	print("login voices.com")
	login_url = "https://www.voices.com/login"
	driver.get(login_url)
	time.sleep(2)
	driver.find_element_by_id('username').send_keys('tarek867656@gmail.com')
	driver.find_element_by_id('password').send_keys('tarek@.com')
	driver.find_element_by_name('sign_in').click()
	time.sleep(2)

	return driver

## list of actor
def actor_list():
	driver = get_driver()
	driver = login(driver)
	a = 0
	## next page
	p = 0
	for i in range(999): 
		print("Next page...")
		url = "https://www.voices.com/talents/search?offset={}".format(a)
		driver.get(url)
		time.sleep(2)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		profile_link = soup.find_all('a', {'class': 'circle-avatar-link'})
		a = a + 10
	
		for url in profile_link:
			profile_url = url.get('href')
			profile(profile_url)
			p = p+1
			print("{} profile data added in json file".format(p))



actor_list()



