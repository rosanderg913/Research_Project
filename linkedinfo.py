from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Function that, given a company name, searches for the LinkedIn page on Google and returns the URL
def search_linkedin_url(company_name):
    query = f"{company_name} linkedin"
    for url in search(query, num_results=1):
        if "linkedin.com/company/" in url:
            return url
    return None

# Function that, given a url to a companys linked in page, parses it for data about company i need
def get_linkedin_info(company_url):
    # Configure the Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

    # Create a WebDriver instance (make sure to have ChromeDriver installed)
    driver = webdriver.Chrome(options=chrome_options)

    # Step 1: Access the LinkedIn company page
    driver.get(company_url)

    # Wait for the page to load (adjust the time based on your needs)
    driver.implicitly_wait(10)

    # Get the page source after JavaScript execution
    company_html = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Step 2: Parse the HTML using BeautifulSoup
    company_soup = BeautifulSoup(company_html, 'html.parser')

    # Extract information from the parsed HTML
    website_link = company_soup.find('a', {'class': 'link-no-visited-state', 'data-tracking-control-name': 'about_website'})
    industry_tag = company_soup.select_one('div[data-test-id="about-us__industry"] dd.font-sans.text-md.text-color-text.break-words.overflow-hidden')
    company_size_tag = company_soup.select_one('div[data-test-id="about-us__size"] dd.font-sans.text-md.text-color-text.break-words.overflow-hidden')

    # Check if any of the information is missing
    if not website_link or not industry_tag or not company_size_tag:
        print(f"Missing information for {company_url}")
        return None

    # Extract the text content from the elements
    website = website_link.text.strip()
    industry_text = industry_tag.text.strip()
    company_size_text = company_size_tag.text.strip()

    return {
        'Linked In': company_url,
        'Website': website,
        'Industry': industry_text,
        'Company Size': company_size_text,
    }
    


# Example usage
# List of company names
company_names = [
    "Colorado Department of Health Care Policy & Financing",
    "Interface, Inc.",
    "EP Global Production Solutions, LLC",
    "The Global Atlantic Financial Group, LLC",
    "Milliman, Inc.",
]

# Iterate over the list of company names
for company_name in company_names:
   # Search for the LinkedIn URL
    linkedin_url = search_linkedin_url(company_name)

    if linkedin_url:
        # Get LinkedIn info for the company
        linkedin_info = get_linkedin_info(linkedin_url)

        if linkedin_info:
            print(f"\nCompany Name -> {company_name}")
            print(f"Linked In -> {linkedin_info['Linked In']}")
            print(f"Website -> {linkedin_info['Website']}")
            print(f"Industry -> {linkedin_info['Industry']}")
            print(f"Company Size -> {linkedin_info['Company Size']}")

