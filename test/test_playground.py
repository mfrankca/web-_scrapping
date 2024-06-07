import requests
from bs4 import BeautifulSoup

URL = 'https://www.ebay.com/itm/' + '186279134509'.strip()
rint('Scraping ' + str(item).strip())
page = requests.get(URL)

print(page.text)

soup = BeautifulSoup(page.content, "html.parser")
#results = soup.find(id="")
img_elements = results.find_all("div", class_="x-photos-min-view filmstrip filmstrip-x")
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()