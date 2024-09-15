from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

# Path to ChromeDriver (manually downloaded)
chrome_driver_path = "./chromedriver.exe"  
chrome_options = Options()
# chrome_options.add_argument("C:/Users/Anushka/AppData/Local/Google/Chrome/User Data/Default")
chrome_options.add_experimental_option("detach", True)
# chrome_driver_path = "C:/Program Files/Google/Chrome/Application/Chrome.exe"  
# Replace with your actual path

# Set up Chrome WebDriver using the manual path
driver = webdriver.Chrome(service=Service(chrome_driver_path),options=chrome_options)

def perform_search(query):
    # Open Google Search
    time.sleep(1)
    driver.get("https://www.google.com")
    
    print(f'driver.command_executor._url: {driver.command_executor._url}')
    print(f'driver.session_id: {driver.session_id}')

    # Find the search input field, enter the query, and submit it
    # search_box = driver.find_element(By.NAME, "q")
    # search_box.clear()
    # for char in query:
    #     search_box.send_keys(char)
    #     time.sleep(random.uniform(0.1, 0.2))  # Random delay between 50ms to 200ms
    
    # search_box.send_keys(Keys.RETURN)  # Press Enter to submit the search

    # Wait for the search results to load
    # time.sleep(3)

    # # Find search result links (CSS selector to locate clickable results)
    # search_results = driver.find_elements(By.XPATH, "//h3/../../a")

    # # Print and click on the first search result
    # if search_results:
    #     print(f"Clicking on the first result for '{query}'")
    #     first_result = search_results[0]
    #     print(f"Title: {first_result.text}")
    #     first_result.click()
    # else:
    #     print(f"No results found for '{query}'")

    # # Wait for the page to load
    # time.sleep(3)

    # Go back to the search results page
    # driver.back()

# List of queries for chained search
queries = ["Latest AI research by google"]

# Perform each search in sequence
for query in queries:
    perform_search(query)

# Close the browser
# driver.quit()
