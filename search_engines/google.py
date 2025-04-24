import requests
from bs4 import BeautifulSoup
import re

def search_google_apis(query, limit=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    urls = []
    for page in range(0, limit):
        start = page * 10
        url = f"https://www.google.com/search?q={query}+API&start={start}"
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and "http" in href:
                match = re.search(r"(https?://[^&]+)", href)
                if match:
                    urls.append(match.group(1))
    return urls