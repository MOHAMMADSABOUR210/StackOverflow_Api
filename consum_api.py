from flask import Flask,request,jsonify
import requests

app = Flask(__name__)


BASE_URL = "https://api.stackexchange.com/2.3"

@app.route('/search')
def search_question():
    query = request.args.get('query')
    url = f"{BASE_URL}/search?order=desc&sort=activity&intitle={query}&site=stackoverflow"
    res = requests.get(url)
    return jsonify(res.json())
