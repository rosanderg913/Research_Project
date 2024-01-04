import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

class Company:
    def __init__(self, name, start_date, end_date, reported_date, pdf=None):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.reported_date = reported_date
        self.pdf = pdf

def extract_data_from_row(driver, row):
    # Find the organization name
    organization_name_xpath = './/td[@class="views-field views-field-field-sb24-org-name"]/a'
    organization_name_element = row.find_element(By.XPATH, organization_name_xpath)
    organization_name = organization_name_element.text

    # Find the date(s) of breach
    dates_of_breach_xpath = './/td[@class="views-field views-field-field-sb24-breach-date"]/span'
    dates_of_breach_elements = row.find_elements(By.XPATH, dates_of_breach_xpath)
    dates_of_breach = []

    for date_element in dates_of_breach_elements:
        # Extract the text content of the span element
        date_text = date_element.text

        # If there's a comma in the text, split into multiple dates
        if ',' in date_text:
            dates_of_breach.extend(date_text.split(','))
        else:
            dates_of_breach.append(date_text)

    # Check if both dates given, substitute 'N/A' if not found
    date_start = dates_of_breach[0] if dates_of_breach else 'N/A'
    date_end = dates_of_breach[1] if len(dates_of_breach) > 1 else 'N/A'

    # Find the reported date
    reported_date_xpath = './/td[@class="views-field views-field-created active"]'
    reported_date = row.find_element(By.XPATH, reported_date_xpath).text

    # Create a Company object
    newCompany = Company(name=organization_name, start_date=date_start, end_date=date_end, reported_date=reported_date)
    
    # Click on the company name (open in a new tab)
    open_company_name_in_new_tab(driver, organization_name_element)

    # Switch to the new tab
    switch_to_new_tab(driver)

    # Extract PDF data
    pdf_path = extract_pdf(driver)

    # Assign pdf to company object
    newCompany.pdf = pdf_path

    # Close the current tab
    close_current_tab(driver)

    # Switch back to the main tab
    switch_to_main_tab(driver)

    # Print the extracted data
    print(f"Company: {newCompany.name}\nBreach Start Date: {newCompany.start_date}\nBreach End Date: {newCompany.end_date}\nReported Date: {newCompany.reported_date}\nPDF: {newCompany.pdf}\n")

    return newCompany

def open_company_name_in_new_tab(driver, organization_name_element):
    # Open the company name link in a new tab using JavaScript
    script = f"window.open('{organization_name_element.get_attribute('href')}', '_blank');"
    driver.execute_script(script)

def switch_to_new_tab(driver):
    # Switch to the new tab
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

def close_current_tab(driver):
    # Close the current tab
    driver.close()

def switch_to_main_tab(driver):
    # Switch to the main tab
    handles = driver.window_handles
    driver.switch_to.window(handles[0])

def extract_pdf(driver):
    try:
        # Wait for the download link to be visible
        pdf_link_xpath = '//div[@class="field-item even"]/span[@class="file"]/a[contains(@href, ".pdf")]'
        pdf_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, pdf_link_xpath)))

        # Get the PDF link and href attribute
        pdf_name = pdf_link.text
        pdf_href = pdf_link.get_attribute("href")
    except NoSuchElementException:
        print("PDF link not found")
        return None

    # Download the PDF
    download_pdf(driver, pdf_href)

    return os.path.join('/Users/gavinrose/Desktop/Research_Project/PDFs/', pdf_name)

def download_pdf(driver, pdf_href):
    # Open the PDF link in a new tab using JavaScript
    script = f"window.open('{pdf_href}', '_blank');"
    driver.execute_script(script)
    time.sleep(5)  # Allow time for the new tab to open and the download to start

# Set up Chrome options to specify the download directory
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": "/Users/gavinrose/Desktop/Research_Project/PDFs/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

# Set up Chrome driver with specified options
driver = webdriver.Chrome(options=chrome_options)

# Example Usage
url = 'https://oag.ca.gov/privacy/databreach/list'
driver.get(url)
time.sleep(1)

rows_xpath = '//tr[@class="even" or @class="odd" or @class="odd views-row-first" or @class="even views-row-first"]'
rows = driver.find_elements(By.XPATH, rows_xpath)

for row in rows[:5]:
    newCompany = extract_data_from_row(driver, row)

# Quit the driver at the end
driver.quit()


####### SWEET SUCCESSSSSSS