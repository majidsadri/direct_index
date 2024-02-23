from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_voo_holdings_selenium(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    wait = WebDriverWait(driver, 20)  # Increased timeout to 20 seconds

    try:
        current_page = 1
        total_pages = 10  # Placeholder for total pages
        while current_page <= total_pages:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            holdings_section = soup.find('div', id='holdings')
            rows = holdings_section.find_all('tr', class_='ng-star-inserted')
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    ticker = cells[0].text.strip()
                    holding_name = cells[1].text.strip()
                    print(ticker, holding_name)

            # Interact with the pagination dropdown
            dropdown_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "vui-select#vui-select-2.vui-select__button")))
            dropdown_button.click()

            # More code here for selecting the next page option
            # ...

            current_page += 1
    except Exception as e:
        print(f"Error on page {current_page}: {str(e)}")
        driver.save_screenshot(f'error_screenshot_{current_page}.png')  # Save a screenshot
        with open(f'error_details_{current_page}.html', 'w') as f:
            f.write(driver.page_source)  # Save the page HTML
        # Optionally, print the HTML of the dropdown or other relevant elements:
        dropdown_html = driver.find_element(By.CSS_SELECTOR, "vui-select#vui-select-2").get_attribute('outerHTML')
        print(dropdown_html)
    finally:
        driver.quit()

voo_url = 'https://investor.vanguard.com/investment-products/etfs/profile/voo#portfolio-composition'
fetch_voo_holdings_selenium(voo_url)
