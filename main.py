import requests
from bs4 import  BeautifulSoup
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


# paras = soup.find_all('p')
# print(paras)

anhor = soup.find_all('a' ,class_="notion-link notion-collection-card__anchor")
print(anhor)