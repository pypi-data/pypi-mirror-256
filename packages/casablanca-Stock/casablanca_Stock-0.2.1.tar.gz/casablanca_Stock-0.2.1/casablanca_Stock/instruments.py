from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd

def Get_instruments(input_text, periode_selection):
    options = Options()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration to avoid potential issues
    options.add_argument('--window-size=1920,1080')  # Set a reasonable window size
    options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images loading

    browser = webdriver.Chrome(options=options)

    browser.get('https://www.casablanca-bourse.com/en/instruments')

    # Find the button element
    button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='autocomplete']"))
    )
    button.click()

    # Find the input field element
    input_field = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Ns:Tout les emetteurs']"))
    )

    # Clear any existing text in the input field
    input_field.clear()

    # Type the desired text into the input field
    input_field.send_keys(input_text)
    input_field.send_keys(Keys.ENTER)

    # Select the dropdown value
    select_dropdown = Select(WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.ID, 'range-date'))
    ))
    select_dropdown.select_by_value(periode_selection)

    # Click the 'Appliquer' button without waiting
    appliquer_button = browser.find_element(By.XPATH, "//button[text()='Apply']")
    appliquer_button.click()

    # Retrieve and return table data using Pandas
    return retrieve_table_data_with_pandas(browser, "//table[contains(@class, 'w-full')]")

# Function to retrieve table data using Pandas
def retrieve_table_data_with_pandas(browser, table_xpath):
    # Wait for a specific element in the table to be present (adjust the XPATH as needed)
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, f"{table_xpath}//tbody/tr"))
    )

    # Retrieve and return table data using Pandas without waiting
    page_source = browser.page_source
    dfs = pd.read_html(page_source)
    
    # Assuming there's a specific DataFrame you want to return, adjust accordingly
    if dfs:
        return dfs[0]  # Returning the first DataFrame
