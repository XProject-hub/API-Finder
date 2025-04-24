from flask import Flask, render_template, request, jsonify
from utils.validator import is_api_alive
from search_engines.google import search_google_apis
from search_engines.github import search_github_apis
from search_engines.public_forums import search_forums
from export import export_to_json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    api_info = {}
    search_results = []
    if request.method == "POST":
        if "search_query" in request.form:
            q = request.form["search_query"]
            google = search_google_apis(q, limit=5)
            github = search_github_apis(q, limit=5)
            forums = search_forums(q, limit=5)
            search_results = list(set(google + github + forums))
            export_to_json(search_results, filename="search_results.json")

        elif "api_url" in request.form:
            url = request.form["api_url"]
            api_info = is_api_alive(url)

    return render_template("index.html", api_info=api_info, search_results=search_results)

if __name__ == "__main__":
    app.run(debug=True)