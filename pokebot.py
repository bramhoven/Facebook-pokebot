import re
import requests
import time
import threading
from requests import Session
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from robobrowser import RoboBrowser

class Pokebot(threading.Thread):
	shutdown = False
	stats = {}
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	browser = RoboBrowser(history=False, parser="lxml")

	def __init__(self, mail, pwd, interval):
		threading.Thread.__init__(self)
		self.mail = mail
		self.pwd = pwd
		self.interval = interval

	def login(self, mail, pwd):
		try:
			self.browser.open("https://facebook.com/login")
			loginform = self.browser.get_form(id="login_form")
			if loginform != None:
				loginform["email"] = mail
				loginform["pass"] = pwd
				self.browser.session.headers["Referer"] = "https://facebook.com/login"
				self.browser.submit_form(loginform)
		except:
			return False

	def check_pokes(self):
		try:
			self.browser.open("https://facebook.com/pokes")
			pokes = self.browser.find_all(id=re.compile('^poke_live_item_'))
			return pokes
		except:
			return []

	def poke(self, pokes):
		for poke in pokes:
			name = poke.find(class_="_42us").find("a").getText() 
			amount = poke.find(class_="_42us").find_all("div")[1].getText().replace(".", "")
			url = poke.find(class_="selected")["ajaxify"]
			try:
				self.browser.open("https://facebook.com/" + url)
				self.set_stat(name, int(re.search(r'\d+', amount).group()))
			except:
				return False

	def set_stat(self, name, amount):
		self.stats[name] = amount
	
	def get_stats(self):
		return self.stats

	def run(self):
		self.login(self.mail, self.pwd)
		while not self.shutdown:
			pokes = self.check_pokes()
			if len(pokes) > 0:
				self.poke(pokes)
			time.sleep(float(self.interval))	