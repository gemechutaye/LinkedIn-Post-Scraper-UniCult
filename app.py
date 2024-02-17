# Import required libraries
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Initialize webdriver 
driver = webdriver.Chrome()

# Login to LinkedIn
driver.get('https://www.linkedin.com')
username = driver.find_element(By.ID, 'session_key')
username.send_keys('username') 
password = driver.find_element(By.ID, 'session_password')
password.send_keys('password')

sign_in_button = driver.find_element(By.CLASS_NAME, 'sign-in-form__submit-button')
sign_in_button.click()

# Wait for login to complete
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "feed-identity-module__actor-meta"))
    )

print("Logged in successfully")

# Scroll to load posts 
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract post text 
posts = driver.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2__description-wrapper > div")
post_text = [post.text for post in posts]

# Store in dataframe
df = pd.DataFrame({'text': post_text})

# Vectorize text 
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(df['text'])

# Cluster using KMeans
num_clusters = 5
km = KMeans(n_clusters=num_clusters) 
km.fit(vectors)
clusters = km.labels_.tolist()

df['cluster'] = clusters 

# Print cluster distribution
print(df.cluster.value_counts())

# Print sample posts per cluster
print(df.groupby('cluster').text.sample(3))