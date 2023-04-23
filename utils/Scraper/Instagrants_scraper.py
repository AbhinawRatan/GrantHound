import requests
from bs4 import BeautifulSoup
import csv


def get_grant_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    grant_data = []
    grant_divs = soup.find_all("div", class_="notion-collection-card gallery")

    for div in grant_divs:
        anchor = div.find("a", class_="notion-link notion-collection-card__anchor")
        content_div = div.find("div", class_="notion-collection-card__content")
        title_div = content_div.find(
            "div", class_="notion-property notion-property__title"
        )
        properties_div = content_div.find(
            "div", class_="notion-collection-card__property-list"
        )

        grant_name = anchor.get_text(strip=True)
        details_link = anchor.get("href")
        application_status = (
            properties_div.find(
                "div",
                class_="notion-property notion-property__select property-77785e41",
            )
            .find("span")
            .get_text(strip=True)
        )
        grant_prize = (
            properties_div.find(
                "div", class_="notion-property notion-property__text property-753d7360"
            )
            .find("span")
            .get_text(strip=True)
        )
        foundation_name = (
            properties_div.find(
                "div",
                class_="notion-property notion-property__select property-4b3c4e76",
            )
            .find("span")
            .get_text(strip=True)
        )
        tags = properties_div.find(
            "div", class_="notion-property notion-property__select property-494c686b"
        ).find_all("span")
        logo = (
            title_div.find("span")
            .find("div")
            .find("span", class_="notion-icon text")
            .get_text(strip=True)
        )
        # title_text = title_div.find("span", class_="").get_text(strip=True)

        grant = {
            "grant_name": grant_name,
            "logo": "",
            "foundation_name": foundation_name,
            "supported_chains": "",
            "application_status": application_status,
            "grant_prize": grant_prize,
            "details_link": "https://superteam.fun" + details_link,
            "application_link": "",
            "description": "",
            "tags": ", ".join([i.get_text(strip=True) for i in tags]),
        }

        # Visit the grant details link to get the description
        if details_link:
            r = requests.get("https://superteam.fun" + details_link)
            soup = BeautifulSoup(r.content, "html.parser")
            anchor_tags = soup.find_all("a", class_="notion-link link")
            for tag in anchor_tags:
                link = tag.get("href")
                if link.startswith("https://airtable.com/"):
                    print(grant_name, "       ------>     ", link)
                    grant["application_link"] = link
            description_divs = soup.find_all("div", {"class": "notion-text"})
            descriptions = [
                "".join([span.text for span in div.find_all("span")])
                for div in description_divs
            ]
            grant["description"] = " ".join(descriptions)

        grant_data.append(grant)

    return grant_data


url = "https://superteam.fun/instagrants"
grant_data = get_grant_data(url)

# Write data to CSV file
with open("grants.csv", mode="a") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "grant_name",
            "logo",
            "foundation_name",
            "supported_chains",
            "application_status",
            "grant_prize",
            "details_link",
            "application_link",
            "description",
            "tags",
        ],
    )
    writer.writeheader()
    for grant in grant_data:
        writer.writerow(grant)
