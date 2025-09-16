import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
from concurrent.futures import ThreadPoolExecutor

URL = "https://www.index.hr/najnovije"
ARTICLE_LINKS = []
HEADERS = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'accept-langage': 'hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7'
}

os.makedirs("htmls", exist_ok=True)

def extract_article_links(URL):
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all("a", class_="vijesti-text-hover scale-img-hover flex")

    for link in links:
        ARTICLE_LINKS.append(f"https://www.index.hr{link.get('href')}")

    print("[INFO] Links extracted.")

    extract_htmls()

def download_article(link_counter):
    link = link_counter
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find("h1", class_="vijesti-text-parsed title js-main-title").get_text(strip=True)
    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)

    todays_date = datetime.today().strftime("%Y%m%d")
    filename = f"htmls/{todays_date}_{safe_title}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    print(f"[SAVED] {filename}")

def extract_htmls():
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_article, ARTICLE_LINKS)

extract_article_links(URL)
