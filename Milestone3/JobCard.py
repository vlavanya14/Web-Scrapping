from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Get the target company name from the user
target_company = input("Enter the target company name: ")

chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.behance.net/joblist?tracking_source=nav20"
driver.get(url)

time.sleep(5)
company_found = False
while not company_found:
    job_cards = driver.find_elements(By.CLASS_NAME, "JobCard-jobCard-mzZ")
    print(f"Number of job cards loaded: {len(job_cards)}")  # Debugging
    for index, card in enumerate(job_cards):
        try:
            company_name = card.find_element(By.CLASS_NAME, "JobCard-company-GQS").text

            if company_name == target_company:
                print(f"Found target company: {company_name} at card index {index + 1}")
                
                card.click()
                time.sleep(5)
                company_found = True
                break  
        except Exception as e:
            print(f"Error checking card {index + 1}: {e}")

    if not company_found:
        print("Scrolling for more job cards...")
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2) 

if not company_found:
    print(f"Company '{target_company}' not found after scrolling.")

if company_found:
    time.sleep(5)  
    print(f"Successfully opened the job details for '{target_company}'.")

# Close the driver
driver.quit()
