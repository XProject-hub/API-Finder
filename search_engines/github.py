import requests
import re

def search_github_apis(query, limit=10):
    headers = {"Accept": "application/vnd.github.v3.text-match+json"}
    api_url = f"https://api.github.com/search/code?q={query}+in:file+extension:py"
    response = requests.get(api_url, headers=headers)
    items = response.json().get("items", [])
    results = []
    for item in items[:limit]:
        raw_url = item['html_url']
        match = re.search(r'https://github\.com/[^/]+/[^/]+', raw_url)
        if match:
            results.append(match.group(0))
    return list(set(results))