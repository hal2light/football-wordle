import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

url = "https://www.transfermarkt.com/super-lig/marktwerte/wettbewerb/TR1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find("table", class_="items")
if table:
    rows = table.find("tbody").find_all("tr", class_=["odd", "even"])
    if rows:
        print("--- FIRST ROW HTML START ---")
        print(rows[0].prettify())
        print("--- FIRST ROW HTML END ---")
else:
    print("Table not found")
