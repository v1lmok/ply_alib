import time
import configparser
import requests
import signal
import json
import os
import sys
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

directory = "C:/2501/ply_Alib/data"
config = configparser.ConfigParser()
config.read(directory + "/settings.ini")
amount = int(config.get("quotesGenerator", "amount"))
init(autoreset=True)

def signal_handler(sig, frame):
    time.sleep(1)
    print(f"\n{Fore.RESET}{Style.DIM}[2501] {Fore.YELLOW}// Shutdown signal received...")
    print(f"{Fore.RESET}{Style.DIM}[2501] {Fore.YELLOW}// Cleaning up...")
    time.sleep(0.5)
    print(f"{Fore.RESET}{Style.DIM}[2501] {Fore.YELLOW}// Thank you for being with us!")
    time.sleep(2)
    sys.exit(0)

def generate_quotes():
    quotes = []
    while len(quotes) < amount:
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
                    print(f"{citata_text} :: {len(quotes)}/{amount}")
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
    print("Saved quotes to json file!")
    time.sleep(3)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print(f"""{Fore.LIGHTWHITE_EX}{Style.DIM}
┌──────────────────┬────────────────────────────────────────────────────────────┐
│     {Fore.RESET}ply_Alib       Quote Generator                                            {Fore.LIGHTWHITE_EX}│
├──────────────────┴────────────────────────────────────────────────────────────┤
│                                                                               │
│{Fore.YELLOW}         ██▓███   ██▓   ▓██   ██▓       ▄▄▄       ██▓     ██▓ ▄▄▄▄             {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}         ▓██░  ██▒▓██▒    ▒██  ██▒      ▒████▄    ▓██▒    ▓██▒▓█████▄          {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}         ▓██░ ██▓▒▒██░     ▒██ ██░      ▒██  ▀█▄  ▒██░    ▒██▒▒██▒ ▄██         {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}         ▒██▄█▓▒ ▒▒██░     ░ ▐██▓░      ░██▄▄▄▄██ ▒██░    ░██░▒██░█▀           {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}         ▒██▒ ░  ░░██████▒ ░ ██▒▓░       ▓█   ▓██▒░██████▒░██░░▓█  ▀█▓         {Fore.LIGHTWHITE_EX}│    
│{Fore.YELLOW}         ▒▓▒░ ░  ░░ ▒░▓  ░  ██▒▒▒        ▒▒   ▓▒█░░ ▒░▓  ░░▓  ░▒▓███▀▒         {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}         ░▒ ░     ░ ░ ▒  ░▓██ ░▒░         ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░▒░▒   ░          {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}         ░░         ░ ░   ▒ ▒ ░░          ░   ▒     ░ ░    ▒ ░ ░    ░          {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}                  ░  ░░ ░                 ░  ░    ░  ░ ░   ░                   {Fore.LIGHTWHITE_EX}│
│{Fore.YELLOW}                      ░ ░                                       ░              {Fore.LIGHTWHITE_EX}│
│                                                                               │
│  {Fore.RESET}[•]   {Fore.GREEN}Welcome to the ply_Alib script!                                        {Fore.LIGHTWHITE_EX}│
│  {Fore.RESET}[!]   {Fore.GREEN}Quotes generating are started!                                         {Fore.LIGHTWHITE_EX}│
│  {Fore.RESET}[!]   {Fore.GREEN}You can change a amount of quotes in {directory}/settings.  {Fore.LIGHTWHITE_EX}│
│  {Fore.RESET}[@]   {Fore.RED}Closing the terminal window is NOT SAFE please use {Fore.RESET}CTRL+C{Fore.RED}.             {Fore.LIGHTWHITE_EX}│
└───────────────────────────────────────────────────────────────────────────────┘
""")
    quotes = generate_quotes()
    save_quotes_to_json(quotes)


if __name__ == "__main__":
    main()
