import json

FILENAME = "htmls/20250916_2709151_33.html"

def read_files():
    with open(FILENAME, "r", encoding="utf-8") as f:
        print(f.read())


read_files()
