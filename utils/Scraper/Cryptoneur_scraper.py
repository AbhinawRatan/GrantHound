import requests
from bs4 import BeautifulSoup
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.cryptoneur.xyz/en/web3-grants/search"

driver = webdriver.Chrome()
driver.get(url)

# find the dropdown element by its class using a CSS selector
dropdown = Select(driver.find_element(by="css selector", value=".select"))

# select the option with value "50"
dropdown.select_by_value("50")

# wait for the page to load and the table rows to be visible
wait = WebDriverWait(driver, 10)
table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bg-base-100")))

# check if the "50" option has been selected
if dropdown.first_selected_option.get_attribute("value") != "50":
    print("Error: Could not select 50 rows")
    driver.quit()
    exit()

# wait for 1 minute before parsing the HTML
time.sleep(10)

# parse the HTML with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# find all the links in the table
table = soup.find("tbody", class_="divide-y divide-base-300 bg-base-100")
table_row = table.find_all("tr")
links = []
for row in table_row:
    link = (
        row.find(
            "td",
            class_="hidden px-4 py-4 text-left text-sm text-base-content/80 lg:table-cell whitespace-normal",
        )
        .find("a")
        .get("href")
    )
    links.append(link)
    print(link)
    print(len(links))

# wait until all the links are printed
wait.until(lambda driver: len(links) == len(table_row))


with open("links.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Link"])
    writer.writerows([[link] for link in links])

# close the browser window
driver.quit()
