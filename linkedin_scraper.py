from selenium import webdriver
from selenium.webdriver.common.by import By
#...import other libraries

driver = webdriver.Chrome()

driver.get('https://www.linkedin.com')
# Find username, password fields and login

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
   time.sleep(3)
   new_height = driver.execute_script("return document.body.scrollHeight")
   if new_height == last_height:
       break
   last_height = new_height