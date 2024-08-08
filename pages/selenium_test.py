import streamlit as st
import requests 
from bs4 import BeautifulSoup 

login_url = "https://signin.ebay.ca/ws/eBayISAPI.dll?SignIn&sgfl=gh&ru=https%3A%2F%2Fwww.ebay.ca%2F" 
login = "reddiveusa@gmail.com" 
password = "Profit44" 

with requests.session() as s: 
	req = s.get(login_url).text 
	html = BeautifulSoup(req,"html.parser") 
	token = html.find("input", {"name": "authenticity_token"}).attrs["value"] 
	time = html.find("input", {"name": "timestamp"}).attrs["value"] 
	timeSecret = html.find("input", {"name": "timestamp_secret"}).attrs["value"] 
 
	payload = { 
		"authenticity_token": token, 
		"login": login, 
		"password": password, 
		"timestamp": time, 
		"timestamp_secret": timeSecret 
	} 
	res =s.post(login_url, data=payload) 
 
	r = s.get(repos_url) 
	soup = BeautifulSoup (r.content, "html.parser") 
	usernameDiv = soup.find("span", class_="p-nickname vcard-username d-block") 
	print("Username: " + usernameDiv.getText()) 
 
	repos = soup.find_all("h3", class_="wb-break-all") 
	for r in repos: 
		repoName = r.find("a").getText() 
		print("Repository Name: " + repoName)