from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set the path to Edge WebDriver
edge_service = Service(r'C:\webdrivers\msedgedriver.exe')

# Initialize WebDriver for Edge
driver = webdriver.Edge(service=edge_service)

# Open LinkedIn and wait for manual login
driver.get("https://www.linkedin.com")

# Wait for user to log in manually before continuing
input("Please log in to LinkedIn manually, then press Enter here to continue...")

# Once logged in, proceed with Google search for profiles
search_query = "site:linkedin.com/in/ AND (CEO OR CFO OR CTO OR COO OR CMO) AND (Facebook OR Amazon OR Apple OR Netflix OR Google)"
driver.get(f"https://www.google.com/search?q={search_query}")
time.sleep(5)

# Extract profile links from Google search results
profiles = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
profile_links = [profile.get_attribute('href') for profile in profiles]

# Lists to store scraped data
job_titles = []
companies = []
industries = []

# Loop through each profile link and extract information
for link in profile_links:
    driver.get(link)
    try:
        # Wait for job title to be visible
        job_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'mt1')]"))
        ).text
        
        # Wait for company name to be visible
        company = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='pv-entity__secondary-title']"))
        ).text
        
        # Wait for industry information to be visible
        industry = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Industry')]"))
        ).text

        job_titles.append(job_title)
        companies.append(company)
        industries.append(industry)

    except Exception as e:
        print(f"Error scraping data for {link}: {e}")
        job_titles.append('N/A')
        companies.append('N/A')
        industries.append('N/A')

# Save scraped data to CSV file
with open('MAANG_executives_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company', 'Industry'])
    for job_title, company, industry in zip(job_titles, companies, industries):
        writer.writerow([job_title, company, industry])

# Keep the browser session open for 1 minute
print("Scraping complete. Browser will stay open for 1 minute.")
time.sleep(60)  # Wait for 60 seconds

# Close browser (after the wait)
driver.quit()
