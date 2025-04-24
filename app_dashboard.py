from flask import Flask, render_template, request
import json, requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def dashboard():
    try:
        with open("ultimate_apis.json") as f:
            apis = json.load(f)
    except:
        apis = []

    category = request.args.get("category")
    source = request.args.get("source")
    keyword = request.args.get("keyword")

    filtered = apis
    if category:
        filtered = [a for a in filtered if category.lower() in a.get("category", "").lower()]
    if source:
        filtered = [a for a in filtered if a.get("source") == source.lower()]
    if keyword:
        filtered = [a for a in filtered if keyword.lower() in a.get("keyword", "").lower()]

    return render_template("dashboard.html", apis=filtered, total=len(filtered))


@app.route("/test", methods=["POST"])
def test_api():
    url = request.form.get("test_url")
    result = "Could not fetch result."
    try:
        r = requests.get(url, timeout=5)
        if "application/json" in r.headers.get("Content-Type", ""):
            result = json.dumps(r.json(), indent=2)
        else:
            result = r.text[:2000]
    except Exception as e:
        result = f"Error: {str(e)}"

    with open("ultimate_apis.json") as f:
        apis = json.load(f)
    return render_template("dashboard.html", apis=apis, total=len(apis), result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
