import requests
from bs4 import  BeautifulSoup

import csv

grant_data = []



url = "https://superteam.fun/instagrants"

# step1: get the html
r = requests.get(url)
htmlContent = r.content
# print(htmlContent)
# step2: parse the html
soup = BeautifulSoup(htmlContent, 'html.parser')
# print(soup.prettify)
# step3: HTML tree traversal
title = soup.title
print(title)

# main page 
divs = soup.find_all('div', class_="notion-collection-card gallery")

for div in divs:
    anchor = div.find("a", class_="notion-link notion-collection-card__anchor")
    content_div = div.find("div", class_="notion-collection-card__content")
    title_div = content_div.find("div", class_="notion-property notion-property__title")
    properties_div = content_div.find("div", class_="notion-collection-card__property-list")
    
    
    
    Grant_name = anchor.get_text(strip=True)
    details_link = anchor.get("href")
    application_status = properties_div.find("div", class_="notion-property notion-property__select property-77785e41").find("span").get_text(strip=True)
    grant_prize = properties_div.find("div",class_="notion-property notion-property__text property-753d7360").find("span").get_text(strip=True)
    foundation_name = properties_div.find("div",class_="notion-property notion-property__select property-4b3c4e76").find("span").get_text(strip=True)
    tags= properties_div.find("div",class_="notion-property notion-property__select property-494c686b").find_all("span")
    
    logo = title_div.find("span").find("div").find("span",class_="notion-icon text").get_text(strip=True)
    title_text = title_div.find("span",class_="").get_text(strip=True)

    print(f"Link: {details_link}\nText: {Grant_name}\nLogo: {logo}\nTitle: {title_text}\nstatus: {application_status}\ngrant_prize: {grant_prize}\nfoundation_name: {foundation_name}\ntags: {tags}\n")
    for i in tags:
        print(i.get_text(strip=True))
    
    grant = {
        "grant_name": Grant_name,
        "details_link": details_link,
        "application_status": application_status,
        "grant_prize": grant_prize,
        "foundation_name": foundation_name,
        "tags": ", ".join([i.get_text(strip=True) for i in tags]),
        "logo": logo,
        "title_text": title_text
    }
    grant_data.append(grant)
        


print(f"{len(grant_data)} grants scraped.")

# Write data to CSV file
with open('grants.csv', mode='w') as file:
    writer = csv.DictWriter(file, fieldnames=["grant_name", "details_link", "application_status", "grant_prize", "foundation_name", "tags", "logo", "title_text"])
    writer.writeheader()
    for grant in grant_data:
        writer.writerow(grant)