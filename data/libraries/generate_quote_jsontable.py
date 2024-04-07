import requests
from bs4 import BeautifulSoup
import json
import os

def generate_citata():
    quotes = []
    while len(quotes) < 10:
        url = "https://finewords.ru/sluchajnaya"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            citata_tag = soup.find('p')
            if citata_tag is not None:
                citata_text = citata_tag.text.strip()
                if len(citata_text) <= 60:
                    quotes.append(citata_text)
        except Exception as e:
            print("Error fetching data:", e)
    return quotes

def save_quotes_to_json(quotes):
    directory = "C:/2501/ply_Alib/data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, "quotes.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(quotes, file, ensure_ascii=False, indent=4)

def main():
    quotes = generate_citata()
    save_quotes_to_json(quotes)

if __name__ == "__main__":
    main()
