import json
from bs4 import BeautifulSoup
import os

FOLDER = "htmls"

def read_files():
    for filename in os.listdir(FOLDER):
        filepath = os.path.join(FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            response = f.read()

            soup = BeautifulSoup(response, 'html.parser')

            title = soup.find("h1", class_="vijesti-text-parsed title js-main-title").getText().strip()
            link = soup.find("link", rel="canonical")["href"]

            # load old JSON (if it exists), otherwise start fresh
            try:
                with open("results.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []

            # create a new entry with id
            new_entry = {
                "id": len(data) + 1,
                "link": link,
                "title": title,
            }
            data.append(new_entry)

            # save back to file
            with open("results.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

read_files()
