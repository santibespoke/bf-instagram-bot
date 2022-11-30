import csv
import requests # to get image from the web
import shutil # to save it locally
import os
from os.path import exists
import xlsxwriter
import html
import validators
import time
import random
import sys
import re
import uuid

#<li>
#	<div class="profile_card">
#		<img src="https://via.placeholder.com/150"/>
#		<p><b>Username: </b>Santi</p>
#		<p><b>Followers: </b>Santi</p>
#		<a target="blank" href="https://instagram.com/bespoke_factory">Link to profile</a>
#	</div>
#</li>

def create_folder_structure():
	#export
	if not os.path.exists('./export'):
		os.makedirs('./export')
	
	#export/requests
	if not os.path.exists('./export/requests'):
		os.makedirs('./export/requests')

	#export/csvs
	if not os.path.exists('./export/csvs'):
		os.makedirs('./export/csvs')
	
	#export/xlsx
	if not os.path.exists('./export/xlsx'):
		os.makedirs('./export/xlsx')
	
	#export/images
	if not os.path.exists('./export/images'):
		os.makedirs('./export/images')
	
def from_human_format(num):
	#remove comma and point
	num = str(num)
	safe = num.replace(',', '') 
	safe = safe.replace('.', '') 

	ret = re.sub("[^0-9]", "", safe)

	p = re.compile(r'[A-Z]')
	letter = p.findall(safe)

	if not letter:
		ret_final = int(ret)
	else:
		if letter[0] == "K":
			ret_final = int(ret) * 1000
		if letter[0] == "M":
			ret_final = int(ret) * 1000000

	return (ret_final)
	

def human_format(num):
	magnitude = 0
	while abs(num) >= 1000:
		magnitude += 1
		num /= 1000.0
	# add more suffixes if you need them
	return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def print_line(file, row):
	print("Printing <li> to html file")
	file.write('<li>\n')
	file.write('<div class="profile_card">\n')
	file.write('<img src="images/'+row["username"]+'.jpg"/>\n')
	file.write('<p class="username"><b>Username: </b>'+row["username"]+'</p>\n')
	file.write('<p class="followers"><b>Followers: </b>'+human_format(int(row["followers"]))+'</p>\n')
	file.write('<a target="blank" href="https://instagram.com/'+row["username"]+'">Link to profile</a>\n')
	file.write('<div>\n')
	file.write('</li>\n')

def excel_print_line(row, s_row, worksheet, followers):
	worksheet.insert_image(s_row, 0, "./export/images/" + row["username"] + ".jpg")

	worksheet.write(s_row, 1, row["username"])
	worksheet.write(s_row, 2, from_human_format(followers))
	worksheet.write(s_row, 3, "https://instagram.com/" + row["username"])
	

def save_image(url, name):

	## Set up the image URL and filename
	image_url = url
	filename = "./export/images/" + name + ".jpg"

	## Check if already exists
	if (exists(filename) == True):
		print("Image " + name + ".jpg already exists, skipping")
		return

	print("Downloading image")
	# Open the url image, set stream to True, this will return the stream content.
	r = requests.get(image_url, stream = True)

	# Check if the image was retrieved successfully
	if r.status_code == 200:
		# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
		r.raw.decode_content = True
        
		# Open a local file with wb ( write binary ) permission.
		with open(filename,'wb') as f:
			shutil.copyfileobj(r.raw, f)
            
		print('Image downloaded to => ',filename)
	else:
		print('Image could not be retreived, sorry')



def get_pic_url(name):

	followers_string = 'na'
	ret_success = True

	## Check if request already exists
	filename = "./export/requests/" + name + ".txt"
	
	if (exists(filename) == True):
		print("Request already exists => " + filename)
		#load request from file
		file = open(filename,mode='r')
		htmlraw = file.read()
		print("Request was loaded from cache")

	else:
		print("Could not find any previous request")
		sleep_for = random.randrange(20000, 60000) / 1000 #Time in miliseconds
		print ("Sleeping for " + str(sleep_for) + " seconds before continuing...")
		time.sleep(sleep_for)
		
		#request html
		insta_url='https://www.instagram.com'
		profile_url = insta_url + "/" + name
		print ("Sending html request")
		response = requests.get(profile_url, headers = {'User-agent': 'your bot 0.1'})
		print ("Response " + str(response.status_code))

		#add error to error count
		global error_count
		if (response.status_code == 200):
			error_count = 0
		else:
			error_count += 1
			print (response.headers)
			

		if response.ok:
			
			htmlraw=response.text
			#save request to file
			with open(filename, "w") as f:
				f.write(response.text)
			print ("Response saved => " + filename)
		else:
			print("Response not valid, terminating request")
			return False, followers_string
		
	#Parse Profile Pic URL
	target = 'meta property="og:image" content="'
	index=htmlraw.find(target)
	remaining_text = htmlraw[index + len(target)  :index + len(target)+650]
	index_end = remaining_text.find('"')
	url_string = remaining_text[0:index_end]
	url_string = url_string.replace('\/', '/')
	url_string = html.unescape(url_string)
	#print("Url profile pic: " + url_string)

	#Parse Followers count
	target_followers = 'Followers'
	index=htmlraw.find(target_followers)
	remaining_text = htmlraw[index - 40  :index + len(target)+200]
	index_start = remaining_text.find('<meta content="')
	index_end = remaining_text.find('Followers')

	followers_string = remaining_text[index_start+15:index_end]
	followers_string = html.unescape(followers_string)
	print("Followers: " + followers_string)
	
	
	

	if (validators.url(url_string,name)== True):
		print("Image URL is fine, initiating request")
		save_image(url_string, name)
	else:
		print("Image URL not valid... skipping")
		return False, followers_string

	return True, followers_string




#Get account name from command arguments
name_target = sys.argv[1]

#Create required directories
create_folder_structure()

#Create a workbook, worksheet, and line controls
workbook = xlsxwriter.Workbook("./export/xlsx/" +name_target+'_'+str(uuid.uuid1())+'.xlsx')
worksheet = workbook.add_worksheet()
s_row = 0
s_col = 0
total_lines = 0
error_count = 0

#Open file and count total lines, to calculate % completed
with open('./export/csvs/'+name_target+'.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		total_lines += 1
print('Total Lines', total_lines + 1)

#Processing the CSV file
with open('./export/csvs/'+name_target+'.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	line_count = 0
	
	for row in csv_reader:
		if line_count == 0:
			print('First csv line')
			line_count += 1
			#Print excel headers on the first line
			worksheet.write(s_row, 0, "Image")
			worksheet.write(s_row, 1, "Username")
			worksheet.write(s_row, 2, "Followers")
			worksheet.write(s_row, 3, "Link")
		else:
			#Calculate completed percentage
			completed = int(((line_count * 100) / total_lines))
			print("Completed: " + str(completed) + '% (line ' + str(line_count) + ' of ' + str(total_lines) + ')')
			print('Processing user => ' + row["username"])
			line_count += 1

			#Main function to request profile page, scrape html, download profile pic, and get follower count
			return_get_pic, followers = get_pic_url(row["username"])

			#Print the line on the spreadsheet
			if (return_get_pic == True):
				s_row += 1
				excel_print_line(row, s_row, worksheet, followers)
				print("Success..!")
			else:
				print("\n******\nWARNING! This line couldn't be processed!\n******\n")

		#Limit the amount of errors
		if (error_count > 1):
			print("\nToo many errors received\n\nTerminating...\n")
			workbook.close()
			quit()

		print("\n--- Errors: " + str(error_count) + " ---\n")
		

