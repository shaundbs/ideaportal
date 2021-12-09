from selenium import webdriver
from selenium.webdriver.chrome.service import Service

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert browser.page_source.find('install')
