import asyncio
import logging
import aiohttp
import random
from data.libraries.animation import animate, clear_animation
from data.libraries.forumEditor import ForumEditor
from data.libraries.random_fact import get_random_fact
from data.libraries.quotes_generate import generate_citata

logging.basicConfig(format='[%(asctime)s] %(levelname)s |   %(message)s', datefmt='%H:%M:%S')

class ForumBioEditor(ForumEditor):
    async def send_bio_request(self, id, choice):
        phrases = ["(☞ﾟヮﾟ)☞", "(∪.∪ )...zzz", "\\(〇_o)/", "ᕦ(ò_óˇ)ᕤ", "(^\\\\\\^)", "( •̀ ω •́ )✧", "\\^o^/",
                   "(❁´◡`❁)", "(*/ω＼*)", "^_^", "╰(*°▽°*)╯", "(¬‿¬)"]
        random_phrase = random.choice(phrases)
        random_quote, author = await generate_citata()
        data = {
            "data": {
                "type": "users",
                "attributes": {
                    "bio": f"Powered by 2501\n"
                },
                "id": str(id)
            }
        }
        if choice == '1':
            data["data"]["attributes"]["bio"] += await get_random_fact()
        elif choice == '2':
            data["data"]["attributes"]["bio"] += random_phrase
        elif choice == '3':
            data["data"]["attributes"]["bio"] += f"Quote: {random_quote}\nAuthor: {author}"
        elif choice == '4':
            choice = random.randint(1, 3)
            if choice == 1:
                data["data"]["attributes"]["bio"] += await get_random_fact()
            elif choice == 2:
                data["data"]["attributes"]["bio"] += random_phrase
            elif choice == 3:
                quote, author = await generate_citata()
                data["data"]["attributes"]["bio"] += f"Quote: {random_quote}\nAuthor: {author}"
        return await self.send_request(id, data)

class ForumNickEditor(ForumEditor):
    async def send_nick_request(self, id, nickname):
        phrases = ["(☞ﾟヮﾟ)☞", "(∪.∪ )...zzz", "\\(〇_o)/", "ᕦ(ò_óˇ)ᕤ", "(^\\\\\\^)", "( •̀ ω •́ )✧", "\\^o^/",
                   "(❁´◡`❁)", "(*/ω＼*)", "^_^", "╰(*°▽°*)╯", "(¬‿¬)"]
        random_phrase = random.choice(phrases)
        random_emoji = chr(random.randint(0x1F600, 0x1F64F))
        choice = random.randint(1, 2)
        data = {
            "data": {
                "type": "users",
                "attributes": {
                    "nickname": f"{nickname} {random_emoji if choice == 1 else random_phrase}"
                },
                "id": str(id)
            }
        }

        return await self.send_request(id, data)

async def Run(id, delay, nickname, choice, senderbio, sendernick):
    loop = 0
    while True:
        animate(delay)
        clear_animation()
        resultbio = await senderbio.send_bio_request(id, choice)
        resultnick = await sendernick.send_nick_request(id, nickname)
        ## await asyncio.sleep(0.1)
        loop = loop + 1
        if not resultbio or not resultnick:
            logging.error(f"[2501] // Error acquired on loop {loop}...")
            break
        print(f"[2501] // Loop: {loop}")

async def fetch_data():
    url = "https://pastebin.com/raw/vdfxN6bp"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return '?.?.?'

async def get_bio(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://forum.wayzer.ru/api/users/{id}") as response:
            data = await response.json()
            bio = data['data']['attributes']['bio']
            return bio
async def main():
    print(f"""
        ██▓███   ██▓   ▓██   ██▓       ▄▄▄       ██▓     ██▓ ▄▄▄▄   
        ▓██░  ██▒▓██▒    ▒██  ██▒      ▒████▄    ▓██▒    ▓██▒▓█████▄ 
        ▓██░ ██▓▒▒██░     ▒██ ██░      ▒██  ▀█▄  ▒██░    ▒██▒▒██▒ ▄██
        ▒██▄█▓▒ ▒▒██░     ░ ▐██▓░      ░██▄▄▄▄██ ▒██░    ░██░▒██░█▀  
        ▒██▒ ░  ░░██████▒ ░ ██▒▓░       ▓█   ▓██▒░██████▒░██░░▓█  ▀█▓
        ▒▓▒░ ░  ░░ ▒░▓  ░  ██▒▒▒        ▒▒   ▓▒█░░ ▒░▓  ░░▓  ░▒▓███▀▒
        ░▒ ░     ░ ░ ▒  ░▓██ ░▒░         ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░▒░▒   ░ 
        ░░         ░ ░   ▒ ▒ ░░          ░   ▒     ░ ░    ▒ ░ ░    ░ 
                 ░  ░░ ░                 ░  ░    ░  ░ ░   ░      
                     ░ ░                                       ░ 

            ply_Alib now in BETA, our current version is {await fetch_data()}
        if you have any questions, please contact the 2501 for help
               turn on debug mode for debugging purposes...
    """)
    ## await asyncio.sleep(0.1)
    yn = str(input('[2501] // Debug mode? [y/n]: '))
    user_id = int(input('[2501] // Enter a ID of user: '))
    biochoice = str(input('[Bio] // Enter your choice (1 for random fact, 2 for random phrase, 3 for random quote, 4 for everytime random): '))
    nickname = str(input('[Nick] // Enter a nickname: '))
    delay = int(input('[2501] // Enter a delay (in seconds): '))
    debug = True if yn.lower() == 'y' else False
    if debug: logging.debug(f'[2501] // Debug mode: {str(debug)}')
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
    if biochoice not in ('1', '2', '3', '4'):
        ## await asyncio.sleep(0.1)
        logging.error(f"[ForumBioEditor] // Error: Enter valid variation...")
        return
    ## await asyncio.sleep(0.1)
    senderbio = ForumBioEditor(debug=debug)
    sendernick = ForumNickEditor(debug=debug)
    await Run(user_id, delay, nickname, biochoice, senderbio, sendernick)


if __name__ == "__main__":
    asyncio.run(main())
