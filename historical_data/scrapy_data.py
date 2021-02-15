from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import random
import time
from datetime import date 

# We need these dates for the range
start_year = date.today().year # This could theroetically be done again in the future
end_year = 1919 # The earliest year of record
count = start_year # Counter for iterating over and changing the year value

# Get the database of information
while count != end_year - 1:
    try:
        # Create a Web Driver with options so I can still work
        options = Options() # Create an options obj
        options.add_argument("--headless") # Wont jump at me
        driver = webdriver.Chrome(options=options) # binary -> executable_path='/usr/bin/chromedriver'

        # Create url for use
        url = f'https://aviation-safety.net/database/dblist.php?Year={count}' # Base URL

        # Wait for the browser to load
        time.sleep(5) # And give the server time

        # Navigate to the page
        driver.get(url) # Open the page

        # Wait for the async table to load and make it random from 30 to 100 to not beat the server up so much
        driver.implicitly_wait(random.sample(range(45, 100), 1)[0]) # This returns a list with an int len of 1

        # Create A DataFrame this will keep from data loss doing every init
        df = pd.read_html(driver.find_element_by_tag_name("table").get_attribute('outerHTML'))[0] # This is a list

        # APPEND Safety Flight Data TO The CSV File So if scrape fails. I can pick up where I left off.
        df.to_csv('flight_safety_data.csv', header=None, mode='a') # Sep doesn't play nice

        # Close the driver
        driver.close() # To not have a million instances open

        # Close the browser
        driver.quit() # To not have a million instances open

        print(f"Added Year:{count}") # So I know it is not just freezing

        # Move to the next year
        count -= 1

    except Exception as e:
        print(e) # Handle errors