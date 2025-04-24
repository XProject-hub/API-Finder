import requests
from bs4 import BeautifulSoup

def search_forums(query, limit=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    urls = []
    search_url = f"https://duckduckgo.com/html/?q={query}+site:reddit.com+OR+site:stackexchange.com"
    resp = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'http' in href and any(site in href for site in ['reddit.com', 'stack']):
            urls.append(href)
            if len(urls) >= limit:
                break
    return urls