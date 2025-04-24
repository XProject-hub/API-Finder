# ultra_auto_search.py
import time
import json
import random
import os
from datetime import datetime
from search_engines.google import search_google_apis
from search_engines.github import search_github_apis
from search_engines.public_forums import search_forums
from search_engines.reddit import search_reddit_apis
from search_engines.rapidapi import search_rapidapi_apis
from utils.validator import is_api_alive, fetch_openapi_spec

KEYWORDS = [
    # SPORTS & LIVE STREAMING
    "live football API", "ESPN API", "SofaScore API", "OneFootball API", "Livescore API",
    "sportsdata.io API", "NBA API", "NFL API", "UEFA API", "FIFA API",
    "MLB API", "NHL API", "cricAPI", "sportsradar API", "football-data.org API",

    # STREAMING / VIDEO
    "YouTube Data API", "Twitch API", "Vimeo API", "Dailymotion API", "Mux video API",
    "JW Player API", "Brightcove API", "Stream API", "Ziggeo video API",

    # CRYPTO & FINANCIAL
    "Binance API", "Coinbase API", "CoinMarketCap API", "CoinGecko API", "CryptoCompare API",
    "Kraken API", "Gemini API", "OpenSea API", "Polygon Finance API", "Alpha Vantage API",
    "IEX Cloud API", "Yahoo Finance API", "Robinhood API", "Nomics API",

    # STOCK / TRADING / INVESTMENT
    "EOD Historical Data API", "MarketStack API", "Finnhub API", "Tiingo API", "Twelve Data API",

    # WEATHER / ENVIRONMENT
    "OpenWeather API", "Weatherstack API", "AccuWeather API", "Climacell API", "AirVisual API",
    "NOAA Weather API", "Windy API", "Meteostat API", "World Weather Online API",

    # GEOLOCATION / TRAVEL
    "Google Maps API", "Here Maps API", "Mapbox API", "TomTom API",
    "Skyscanner API", "Amadeus API", "FlightAware API", "Trip.com API",
    "OpenStreetMap API", "Geoapify API",

    # SOCIAL / MESSAGING / MEDIA
    "Twitter API", "Telegram Bot API", "Reddit API", "Discord Bot API", "Slack API",
    "Facebook Graph API", "Instagram Graph API", "WhatsApp Business API",
    "YouTube Data API", "TikTok API",

    # AI / GPT / ML
    "OpenAI API", "ChatGPT API", "Anthropic Claude API", "Cohere API", "Replicate API",
    "HuggingFace API", "Stability AI API", "AssemblyAI API", "Deepgram API", "Google PaLM API",

    # NEWS / CONTENT / DATA
    "NewsAPI", "ContextualWeb API", "Bing News API", "GNews API", "Event Registry API",
    "Guardian API", "NYTimes Developer API", "Wordnik API", "Wikipedia API",

    # HEALTH / SCIENCE
    "OpenFDA API", "NHS UK API", "CDC Data API", "HealthCare.gov API", "Nutritionix API",
    "PubChem API", "DrugBank API", "ClinicalTrials.gov API", "NASA API", "OpenAI research API",

    # ECOMMERCE
    "Amazon Product API", "eBay Developer API", "Walmart API", "BestBuy API",
    "Shopify API", "BigCommerce API", "Stripe API", "PayPal API", "Square API",

    # TOOLS / UTILITIES
    "ipapi", "ipinfo.io", "Numverify API", "Abstract API", "Apilayer API",
    "Clearbit API", "Kickbox Email API", "mailboxlayer", "WhoisXML API", "SerpAPI",
    "URLScan API", "VirusTotal API", "Google Safe Browsing API", "Shodan API",

    # CLOUD / AUTH / STORAGE
    "Firebase API", "AWS API", "Google Cloud API", "Dropbox API", "OneDrive API",
    "Auth0 API", "Okta API", "Cloudflare API", "DigitalOcean API",

    # DEV TOOLS
    "Postman Public API", "RapidAPI Public Hub", "GitHub API", "GitLab API", "Bitbucket API",
    "Docker Hub API", "NPM Registry API", "PyPI API", "Jira API", "Notion API", "Trello API",

    # SEARCH / AI / TRANSLATION
    "Google Custom Search API", "SerpAPI", "Microsoft Translator API", "DeepL API",
    "Google Cloud Translation API", "LibreTranslate API", "Bing Search API"
]

KNOWN_APIS = {
    "coinmarketcap": "CoinMarketCap API",
    "coingecko": "CoinGecko API",
    "youtube": "YouTube Data API",
    "reddit": "Reddit API",
    "openweather": "OpenWeather API",
    "openai": "OpenAI API",
    "twitch": "Twitch API",
    "twitter": "Twitter API",
    "shopify": "Shopify API",
    "stripe": "Stripe API"
}

RESULT_FILE = "ultimate_apis.json"
BACKUP_DIR = "backups/"
DELAY_SECONDS = 300

def load_results():
    try:
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_results(results):
    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=2)

def backup_results():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{BACKUP_DIR}backup_{now}.json"
    with open(filename, "w") as f:
        json.dump(load_results(), f, indent=2)

def search_everywhere(keyword):
    google = search_google_apis(keyword, limit=8)
    github = search_github_apis(keyword, limit=8)
    forums = search_forums(keyword, limit=8)
    reddit = search_reddit_apis(keyword, limit=8)
    rapid = search_rapidapi_apis(keyword, limit=8)
    return set(google + github + forums + reddit + rapid)

def categorize_link(link):
    for keyword in KEYWORDS:
        if any(k in link.lower() for k in keyword.split()):
            return keyword
    return "uncategorized"

def run_ultra_loop():
    known = {entry['url'] for entry in load_results()}
    data = load_results()
    iteration = 0

    print("🔁 Ultimate API Finder started!")

    while True:
        keyword = random.choice(KEYWORDS)
        print(f"\n🔍 Searching for: {keyword}")

        new_links = search_everywhere(keyword)
        new_entries = []

        for url in new_links:
            if url not in known:
                verify = is_api_alive(url)
                if 'error' not in verify and verify.get("status") == 200:
                    source_tag = next((name for name in KNOWN_APIS if name in url.lower()), None)
                    entry = {
                        "url": url,
                        "status": verify["status"],
                        "content_type": verify.get("content_type", ""),
                        "category": categorize_link(url),
                        "keyword": keyword,
                        "source": source_tag,
                        "timestamp": datetime.now().isoformat()
                    }
                    spec = fetch_openapi_spec(url)
                    if spec:
                        entry["openapi"] = True
                        entry["spec_sample"] = list(spec.keys())[:5]
                    new_entries.append(entry)
                    known.add(url)
                    print(f"✅ Found: {url}")
                else:
                    print(f"❌ Skipped (bad response): {url}")

        if new_entries:
            data.extend(new_entries)
            save_results(data)

        iteration += 1
        if iteration % 12 == 0:
            backup_results()
            print("💾 Backup created!")

        print(f"⏳ Sleeping {DELAY_SECONDS} sec...")
        time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    run_ultra_loop()