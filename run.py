from search_engines.google import search_google_apis
from api_tester import test_api

def main():
    print("=== API Finder - CLI ===")
    q = input("🔍 Enter search keyword: ")
    results = search_google_apis(q)
    for i, url in enumerate(results):
        print(f"{i+1}. {url}")
    choice = int(input("Choose an API to test (number): ")) - 1
    test_api(results[choice])

if __name__ == "__main__":
    main()
