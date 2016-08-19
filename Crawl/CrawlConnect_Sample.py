from selenium import webdriver
import os

chromedriver = "/users/rutherfordle/PycharmProjects/Crawl/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
#driver = webdriver.Chrome()
driver.get('https://pulse.conviva.com/login?next=/reports/15/')
username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys("username")
password.send_keys("password")

