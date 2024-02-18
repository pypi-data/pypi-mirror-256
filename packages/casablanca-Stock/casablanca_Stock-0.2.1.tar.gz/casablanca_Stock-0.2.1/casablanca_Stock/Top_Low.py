from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from fake_useragent import UserAgent
import random

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def Get_Low_high(index):
    # Set up the Selenium webdriver
    url= 'https://www.casablanca-bourse.com/fr/live-market/overview'

    options = Options()
    options.add_argument("--headless")   # Run in headless mode (no browser window)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Get a random user agent
    user_agent = get_random_user_agent()
    options.add_argument(f'user-agent={user_agent}')

    try:
        driver = webdriver.Chrome(options=options)

        # Open the webpage
        driver.get(url)

        # Wait for JavaScript to execute (adjust the time based on the webpage)
        driver.implicitly_wait(10)

        # Extract data using pandas
        tables = pd.read_html(driver.page_source)

        # Check if any tables are found
        if tables:
            # Assuming the table of interest is the first one on the page
            table_data = tables[index]  # Assuming the first table

            # Check if the DataFrame is empty
            if not table_data.empty:
                # Print the DataFrame
                return table_data # Return if DataFrame is not empty to skip scraping with the next agent
            else:
                print("DataFrame is empty. Proceeding with the next agent.")
        else:
            print("No tables found on the page.")
    except Exception as e:
        print("Error:", str(e))
    finally:
        # Close the webdriver in a 'finally' block to ensure it gets closed even if an exception occurs
        driver.quit()

# Example usage:


'''getting lower performance of the day '''
# Specify the number of random user agents you want
num_user_agents = 3
def Get_Low(index):
    index=0
    for _ in range(num_user_agents):
        df=Get_Low_high(index)
        if df.empty:
            pass
        else: 
            return df
'''geting higher action of the day '''
def Get_High(index):
    index=1
    for _ in range(num_user_agents):
        df=Get_Low_high(index)
        if df.empty:
            pass
        else: 
            return  df


