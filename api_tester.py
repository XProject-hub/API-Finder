from utils.validator import is_api_alive

def test_api(api_url):
    result = is_api_alive(api_url)
    if "error" in result:
        print(f"[ERROR] {result['error']}")
    else:
        print(f"✅ Status: {result['status']}")
        print(f"📦 Content-Type: {result['content_type']}")
        if result["json"]:
            print("🔎 JSON Preview:")
            for key, val in result["json"].items():
                print(f"  - {key}: {val}")
