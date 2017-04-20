import re
import getpass
import threading
import requests
import time
from requests import Session
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from robobrowser import RoboBrowser

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
browser = RoboBrowser(history=False, parser="lxml")

def login(mail, pwd):
	browser.open("https://facebook.com/login")
	loginform = browser.get_form(id="login_form")
	loginform["email"] = mail
	loginform["pass"] = pwd
	browser.session.headers["Referer"] = "https://facebook.com/login"
	browser.submit_form(loginform)
	print "Logged in\n"

def check_pokes():
	browser.open("https://facebook.com/pokes")
	pokes = browser.find_all(id=re.compile('^poke_live_item_'))
	return pokes

def facebook_poke(pokes):
	for poke in pokes:
		name = poke.find(class_="_42us").find("a").getText() 
		amount = poke.find(class_="_42us").find_all("div")[1].getText()
		url = poke.find(class_="selected")["ajaxify"]
		browser.open("https://facebook.com/" + url)

		print "----------------"
		print name
		print amount
		print "Poked him back"
		print "----------------\n"

def facebook_run(mail, pwd, interval):
	while True:
		pokes = check_pokes()
		if len(pokes) > 0:
			facebook_poke(pokes)
		time.sleep(float(interval))
      
    

if __name__ == "__main__":
	mail = raw_input("Email: ")
	pwd = getpass.getpass("Password: ")
	interval = raw_input("Interval: ")
	login(mail, pwd)

	threading.Thread(interval, facebook_run(mail, pwd, interval)).start()
