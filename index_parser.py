import json
from bs4 import BeautifulSoup
import os
import re
import time

FOLDER = "htmls"

def read_files():
    start = time.time()
    counter = 0

    for filename in os.listdir(FOLDER):
        filepath = os.path.join(FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            response = f.read()

            soup = BeautifulSoup(response, 'html.parser')

            title = soup.find("h1", class_="vijesti-text-parsed title js-main-title").getText(strip=True)
            safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
            link = soup.find("link", rel="canonical")["href"]
            published_date = soup.find("div", class_="flex-1").find_all("div")[-1].get_text(strip=True).replace("Zadnja nadopuna:", "").strip()
            description = soup.find("div", class_="text-holder").get_text(strip=True)

            # load old JSON (if it exists), otherwise start fresh
            try:
                with open("results.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []

            # create a new entry with id
            new_entry = {
                # "id": len(data) + 1,
                "link": link,
                "title": safe_title,
                "published date": published_date,
                "description": description,
            }

            # don't add if link already exists
            if not any(entry["link"] == link for entry in data):
                data.append(new_entry)
                counter += 1

            # save back to file
            with open("results.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Added {counter} new file(s) to results.json")
    end = time.time()

    print(f"{end-start:.2f} seconds")

read_files()
