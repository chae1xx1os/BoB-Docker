import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from database import get_db
from models import Friend

def scrape_and_save_friend_info(url: str, db: Session):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find("h1", class_="firstHeading").text.strip()
        description = soup.find("div", class_="mw-parser-output").text.strip()
        
        new_friend = Friend(name=name, specialty="개발보안", description=description)
        db.add(new_friend)
        db.commit()
    else:
        print(f"Failed to retrieve page: {url}")

urls = [
    "https://kitribob.wiki/wiki/김태양",
    "https://kitribob.wiki/wiki/전성현",
    "https://kitribob.wiki/wiki/하진우",
    "https://kitribob.wiki/wiki/김채영",
    "https://kitribob.wiki/wiki/이산",
    "https://kitribob.wiki/wiki/송현준",
]

with get_db() as db:
    for url in urls:
        scrape_and_save_friend_info(url, db)
