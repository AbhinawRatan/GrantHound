# import requests
# from bs4 import BeautifulSoup
# import csv


# url = "https://www.cryptoneur.xyz/en/"


# # getting links from  links.csv
# with open("links.csv", "r") as file:
#     reader = csv.reader(file)
#     next(reader)  # Skip the header row
#     for row in reader:
#         link = row[0]

#         # Make a request to the link and parse the HTML content with Beautiful Soup
#         response = requests.get(url + link)
#         soup = BeautifulSoup(response.content, "html.parser")

#         links = soup.find(
#             "div",
#             class_="mt-6 flex flex-col-reverse justify-stretch space-y-4 space-y-reverse sm:flex-row-reverse sm:justify-end sm:space-x-3 sm:space-y-0 sm:space-x-reverse md:mt-0 md:flex-row md:space-x-3",
#         )
#         logo = soup.find(
#             "div",
#             class_="mx-auto max-w-3xl px-4 sm:px-6 md:flex md:items-center md:justify-between md:space-x-5 lg:max-w-7xl lg:px-8",
#         ).find("img")["src"]
#         # print("https://www.cryptoneur.xyz" + logo)

#         foundation_name = soup.find("h1", class_="text-2xl font-bold").text

# application_status = (
#     soup.find("p", class_="text-sm font-medium text-base-content/80")
#     .find("time")
#     .text
# )
#         print(application_status)
#         details_link = links.find("a", class_="btn-outline btn-primary btn")["href"]
#         application_link = links.find("a", class_="btn-primary btn")["href"]

#         description = soup.find("dd", class_="mt-1 text-sm text-base-content").text
#         tags = soup.find_all(
#             "div",
#             class_="sm:col-span-2",
#         )
#         for tag in tags:
#             if (
#                 tag.find("dt", class_="text-sm font-medium text-base-content/80").text
#                 == "Grant Category"
#             ):
#                 spans = tag.find(
#                     "dd", class_="mt-1 flex flex-wrap gap-2 text-sm text-base-content"
#                 ).find_all(
#                     "span",
#                     class_="inline-flex items-center rounded-full bg-primary px-3 py-0.5 text-sm font-medium text-primary-content",
#                 )
#                 for span in spans:
#                     print(span.text)
#             else:
#                 continue

# minimum_grant = soup.find("div", class_="sm:col-span-1")
# if minimum_grant is None:
#     continue
# else:
#     if (
#         minimum_grant.find(
#             "dt", class_="text-sm font-medium text-base-content/80"
#         ).text
#         == "Minimum Funding"
#     ):
#         print(
#             minimum_grant.find(
#                 "dd", class_="mt-1 text-sm text-base-content"
#             ).text
#         )
#     else:
#         print("No minimum funding")

# maximum_grant = soup.find("div", class_="sm:col-span-1")
# if maximum_grant is None:
#     continue
# else:
#     if (
#         maximum_grant.find(
#             "dt", class_="text-sm font-medium text-base-content/80"
#         ).text
#         == "Maximum Funding"
#     ):
#         print(
#             maximum_grant.find(
#                 "dd", class_="mt-1 text-sm text-base-content"
#             ).text
#         )
#     else:
#         print("No maximum funding")


import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cryptoneur.xyz/en/"

# getting links from  links.csv
with open("links.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    with open("backend/grants.csv", mode="a") as outfile:
        writer = csv.DictWriter(
            outfile,
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

        for row in reader:
            link = row[0]

            # Make a request to the link and parse the HTML content with Beautiful Soup
            response = requests.get(url + link)
            soup = BeautifulSoup(response.content, "html.parser")

            chains = soup.find_all(
                "div",
                class_="sm:col-span-2",
            )

            chain_list = []
            for chain in chains:
                if (
                    chain.find(
                        "dt", class_="text-sm font-medium text-base-content/80"
                    ).text
                    == "Supported Blockchains"
                ):
                    spans = chain.find(
                        "dd",
                        class_="mt-1 flex flex-wrap gap-2 text-sm text-base-content",
                    ).find_all(
                        "span",
                        class_="inline-flex items-center rounded-full bg-primary px-3 py-0.5 text-sm font-medium text-primary-content",
                    )
                    for span in spans:
                        chain_list.append(span.text)
                        print(span.text)
                else:
                    continue

            links = soup.find(
                "div",
                class_="mt-6 flex flex-col-reverse justify-stretch space-y-4 space-y-reverse sm:flex-row-reverse sm:justify-end sm:space-x-3 sm:space-y-0 sm:space-x-reverse md:mt-0 md:flex-row md:space-x-3",
            )
            logo = soup.find(
                "div",
                class_="mx-auto max-w-3xl px-4 sm:px-6 md:flex md:items-center md:justify-between md:space-x-5 lg:max-w-7xl lg:px-8",
            ).find("img")["src"]

            foundation_name = soup.find("h1", class_="text-2xl font-bold").text
            print(foundation_name)
            application_status = (
                soup.find("p", class_="text-sm font-medium text-base-content/80")
                .find("time")
                .text
            )

            details_link = links.find("a", class_="btn-outline btn-primary btn")["href"]
            application_link = links.find("a", class_="btn-primary btn")["href"]

            description = soup.find("dd", class_="mt-1 text-sm text-base-content").text
            tags = soup.find_all(
                "div",
                class_="sm:col-span-2",
            )

            tags_list = []
            for tag in tags:
                if (
                    tag.find(
                        "dt", class_="text-sm font-medium text-base-content/80"
                    ).text
                    == "Grant Category"
                ):
                    spans = tag.find(
                        "dd",
                        class_="mt-1 flex flex-wrap gap-2 text-sm text-base-content",
                    ).find_all(
                        "span",
                        class_="inline-flex items-center rounded-full bg-primary px-3 py-0.5 text-sm font-medium text-primary-content",
                    )
                    for span in spans:
                        tags_list.append(span.text)
                else:
                    continue
                print("printing grants---------------------------------")
                minf = ""
                maxf = ""
                grant = soup.find_all("div", class_="sm:col-span-1")
                for i in grant:
                    if (
                        i.find(
                            "dt", class_="text-sm font-medium text-base-content/80"
                        ).text
                        == "Minimum Funding"
                    ):
                        minf = i.find(
                            "dd", class_="mt-1 text-sm text-base-content"
                        ).text
                    elif (
                        i.find(
                            "dt", class_="text-sm font-medium text-base-content/80"
                        ).text
                        == "Maximum Funding"
                    ):
                        maxf = i.find(
                            "dd", class_="mt-1 text-sm text-base-content"
                        ).text

                # Check if minf and maxf have been defined, and combine them into a string
                if "minf" in locals() and "maxf" in locals():
                    prize = minf + "  " + maxf
                    print(prize)
                    minf = ""
                    maxf = ""
                else:
                    prize = "N/A"
                    print(prize)
                    minf = ""
                    maxf = ""

            grant = {
                "grant_name": foundation_name,
                "logo": "https://www.cryptoneur.xyz" + logo,
                "foundation_name": foundation_name,
                "supported_chains": ", ".join(chain_list),
                "application_status": application_status,
                "grant_prize": prize,
                "details_link": details_link,
                "application_link": application_link,
                "description": description,
                "tags": ", ".join(tags_list),
            }

            writer.writerow(grant)
