from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config import SCRAPE_DELAY
import time
# ...existing code...
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_top_10_coins(headless=True):
    # Set up Chrome options
    options = Options()
    if headless:
        # use new headless mode for newer Chrome versions
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # simple user-agent to reduce bot blocking
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Launch browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://coinmarketcap.com/")

    # Wait for table rows to appear (use SCRAPE_DELAY as max wait)
    wait_timeout = max(10, SCRAPE_DELAY)
    try:
        wait = WebDriverWait(driver, wait_timeout)
        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
    except Exception as e:
        print(f"Error waiting for rows: {e}")
        driver.quit()
        return []

    # take top 10 rows
    rows = rows[:10]
    coins_data = []

    for row in rows:
        try:
            # Use td indexing to reduce reliance on brittle XPaths
            tds = row.find_elements(By.TAG_NAME, "td")
            name = ""
            price = ""
            change = ""
            market_cap = ""

            if len(tds) > 2:
                try:
                    name = tds[2].find_element(By.TAG_NAME, "p").text
                except:
                    name = tds[2].text.strip()

            if len(tds) > 3:
                try:
                    price = tds[3].find_element(By.TAG_NAME, "span").text
                except:
                    price = tds[3].text.strip()

            if len(tds) > 4:
                try:
                    change = tds[4].find_element(By.TAG_NAME, "span").text
                except:
                    change = tds[4].text.strip()

            if len(tds) > 6:
                try:
                    market_cap = tds[6].find_element(By.TAG_NAME, "p").text
                except:
                    market_cap = tds[6].text.strip()

            coins_data.append({
                "Name": name,
                "Price": price,
                "24h Change": change,
                "Market Cap": market_cap
            })
        except Exception as e:
            print(f"Error scraping row: {e}")

    driver.quit()
    return coins_data

