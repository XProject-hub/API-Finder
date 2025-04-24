from search_engines.google import search_google_apis
from search_engines.github import search_github_apis
from search_engines.public_forums import search_forums
from api_tester import test_api

print("=== API Finder CLI ===")
q = input("🔍 Enter keyword (e.g. weather, payment): ")
google = search_google_apis(q, limit=5)
github = search_github_apis(q, limit=5)
forums = search_forums(q, limit=5)
all_results = list(set(google + github + forums))
for i, url in enumerate(all_results):
    print(f"{i+1}. {url}")
if all_results:
    choice = int(input("Choose an API to test (number): ")) - 1
    test_api(all_results[choice])
else:
    print("No APIs found.")