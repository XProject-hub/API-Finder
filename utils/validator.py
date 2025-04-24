import requests

def is_api_alive(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", ""),
            "json": response.json() if "application/json" in response.headers.get("Content-Type", "") else None
        }
    except Exception as e:
        return {"error": str(e)}