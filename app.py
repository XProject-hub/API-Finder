from flask import Flask, render_template, request
from utils.validator import is_api_alive

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    api_info = {}
    if request.method == "POST":
        api_url = request.form["api_url"]
        api_info = is_api_alive(api_url)
    return render_template("index.html", api_info=api_info)

if __name__ == "__main__":
    app.run(debug=True)
