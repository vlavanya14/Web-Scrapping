from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

chrome_options = Options()
chrome_options.add_argument("--start-fullscreen") 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.behance.net/joblist?tracking_source=nav20"
driver.get(url)

# time.sleep(5)  # Ensure sufficient time for the page to load

for _ in range(3):  # Number of scrolls
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

# Find all job cards
job_cards = driver.find_elements(By.CLASS_NAME, "JobCard-jobCard-mzZ")
print(f"Number of job cards found: {len(job_cards)}")  # Debugging

data = []


for index, card in enumerate(job_cards):
    try:
        company = card.find_element(By.CLASS_NAME, "JobCard-company-GQS").text
        title = card.find_element(By.CLASS_NAME, "JobCard-jobTitle-LS4").text
        description = card.find_element(By.CLASS_NAME, "JobCard-jobDescription-SYp").text
        time_posted = card.find_element(By.CLASS_NAME, "JobCard-time-Cvz").text
        location = card.find_element(By.CLASS_NAME, "JobCard-jobLocation-sjd").text
        image_element = card.find_element(By.CLASS_NAME, 'JobLogo-logoButton-aes').find_element(By.TAG_NAME, 'img')
        image_url = image_element.get_attribute('src')

        data.append([company, title, description, time_posted, location, image_url])
      
    except Exception as e:
        print(f"Error extracting job details for card {index + 1}: {e}")

# Save to CSV
if data:
    filename = "behance_jobs.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Job Title", "Description", "Time Posted", "Location", "image_url"])  # Header
        writer.writerows(data)
    print(f"Data saved to {filename}")
else:
    print("No data to save.")

# Close the driver
driver.quit()