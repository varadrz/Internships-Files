import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://www.linkedin.com/login')

email = driver.find_element(By.ID, 'username')
email.send_keys(' ')                                        #enter your email ID
password = driver.find_element(By.ID, 'password')
password.send_keys(' ')                                     #enter your password
password.send_keys(Keys.RETURN)

time.sleep(5)

search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
search_box.send_keys('IIT graduate')
search_box.send_keys(Keys.RETURN)

time.sleep(5)

with open('iit_graduates_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Job Title', 'Company', 'Industry'])

    for page in range(3):
        profiles = driver.find_elements(By.CLASS_NAME, 'entity-result__item')

        for profile in profiles:
            profile_html = profile.get_attribute('outerHTML')
            soup = BeautifulSoup(profile_html, 'html.parser')

            try:
                name = soup.find('span', {'class': 'entity-result__title-text'}).get_text(strip=True)
            except AttributeError:
                name = "Not Available"

            try:
                job_title = soup.find('div', {'class': 'entity-result__primary-subtitle'}).get_text(strip=True)
            except AttributeError:
                job_title = "Not Available"

            try:
                company = soup.find('div', {'class': 'entity-result__secondary-subtitle'}).get_text(strip=True)
            except AttributeError:
                company = "Not Available"

            industry = "Not Available"

            writer.writerow([name, job_title, company, industry])

        try:
            next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
            next_button.click()
            time.sleep(5)
        except Exception as e:
            break

driver.quit()

print("Scraping completed. Data saved to 'iit_graduates_data.csv'.")
