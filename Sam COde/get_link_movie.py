from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, keyboard

driver = webdriver.Firefox()
# URL = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2006-01-01&sort=user_rating,desc&num_votes=1000,'
# URL = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2006-01-01,2006-01-01&sort=user_rating,desc&num_votes=1000,'
URL = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2008-08-01&sort=user_rating,desc&num_votes=1000,'
driver.get(URL)

i = 0
while True:
	try:
		if i == 133 or keyboard.is_pressed('q'):
			break
		button = driver.find_elements(By.XPATH, '//button[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--on-accent2 ipc-text-button ipc-see-more__button"]')
		button[0].location_once_scrolled_into_view
		time.sleep(0.5)
		button[0].click()
		time.sleep(3)
		i += 1
	except Exception as error:
		print(i)
		time.sleep(10)

links = driver.find_elements(By.XPATH, '//a[@class="ipc-lockup-overlay ipc-focusable"]')
with open('Movie_Link.txt', 'a') as f:
	for link in links:
		text = link.get_attribute('href')
		f.write(f'{text}\n')

driver.close()