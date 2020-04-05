import requests
import bs4
import re
import pandas as pd
import np
import os

def get_title(soup):
	return soup.find('h1').next_element

def get_page(nb):
	token = 'http://www.test.com/=' # TO CHANGE
	return token + str(nb)

def get_email(text):
	domains = ["fr", "com", "net", "org"]
	for domain in domains:
		email = list(set(re.findall("[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\."+domain, text, re.I)))
		if len(email) > 0:
			return email[0]

def get_zipCode(text):
	possibleZipCodeLengths = [5,2]
	for length in possibleZipCodeLengths:
		zipCodeWithPrefix = list(set(re.findall("Code postal : \d{" + str(length) + "}", text, re.I)))
		if len(zipCodeWithPrefix) > 0:
			zipCode = list(set(re.findall("\d{" + str(length) + "}", str(zipCodeWithPrefix[0]), re.I)))
			if len(zipCode) > 0:
				return zipCode[0]

def save_to_csv(title, emails, zipCodes):
    if len(emails) == 0 and len(zipCodes) == 0:
        return

    folder = "results/"
    if not(os.path.exists(folder)):
        os.mkdir(folder)

    df = pd.DataFrame({"Emails" : np.array(emails), "Codes postaux" : np.array(zipCodes)})
    fileName = "results/" + title + ".csv"
    df.to_csv(fileName, index=False)
    print("Process page : " + title + " SUCCEED")

def parse_page(num_page):
	response = requests.get(get_page(num_page))
	if response.status_code != 200:
	    return
	soup = bs4.BeautifulSoup(response.text, 'html.parser')
	title = get_title(soup)
	posts = list(soup.find_all("ul"))
	emails = list()
	zipCodes = list()
	for post in posts:
	    email = str(get_email(post.text))
	    zipCode = str(get_zipCode(post.text))
	    if email != "None" and zipCode != "None":
	        emails.append(email)
	        zipCodes.append(zipCode)
	
	save_to_csv(title, emails, zipCodes)

# main
for i in range(0,200):
	parse_page(i)
