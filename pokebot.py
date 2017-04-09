from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sys
import getpass
import threading
import docker
from random import randint

client = docker.from_env()
containers = client.containers()
seleniums = [c for c in containers if c["Image"] == "danielfrg/selenium"]

def start():
	email = raw_input("Email: ")
	password = getpass.getpass("Password: ") 
	interval = raw_input("Seconds between checks: ")
	print ""
	print "Let's get ready to poke!"
	print ""

	runBot(email, password, interval)
	driver.quit()

def facebook_login(email, pwd):
	driver.get("https://www.facebook.com/login")
	email = driver.find_element_by_css_selector("#email").send_keys(email)
	password = driver.find_element_by_css_selector("#pass").send_keys(pwd)
	login = driver.find_element_by_css_selector("#loginbutton").submit()
	return True

def facebook_checkpokes():
	pokes = driver.find_elements_by_xpath("//div[contains(@id, 'poke_live_item_')]")
	return pokes

def facebook_run(email, password, interval):
	global driver


	selenium = seleniums[randint(0, len(seleniums)-1)]
	try:
		driver = webdriver.Remote(command_executor="http://127.0.0.1:"+str(selenium["Ports"][0]["PublicPort"])+"/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
		facebook_login(email, password)
		driver.get("https://www.facebook.com/pokes/")
		if driver.find_element_by_xpath("//a[contains(@href,'/pokes/')]"):
			pokes = facebook_checkpokes() 
			infos = []

			if pokes != None: 
				for poke in pokes:
					textdiv = poke.find_element_by_css_selector("._6a._42us")
					name = textdiv.find_element(By.TAG_NAME, "a").text.encode("utf-8")
					amount = textdiv.find_elements(By.TAG_NAME, "div")[1].text.encode("utf-8")
					button = poke.find_element_by_css_selector(".selected")
					link = button.get_attribute("ajaxify")
					infos.append((name, amount, link))

			for info in infos:
				print "---------------"
				print info[0], info[1]
				print "Poked him back"
				print "---------------"
				print ""
				driver.get("https://facebook.com" + info[2])
	except:
		print "Something went wrong"
		print "Restarted container: " + selenium.id
		selenium.restart()
	finally:
		driver.quit()
		threading.Timer(interval, facebook_run(email, password, interval)).start()

def runBot(email, password, interval):
	facebook_run(email, password, interval)

if __name__ == "__main__":
    start()
