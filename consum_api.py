from flask import Flask, request, jsonify
import requests
import csv  
import os  

app = Flask(__name__)


BASE_URL = "https://api.stackexchange.com/2.3"

app = Flask(__name__)
BASE_URL = "https://api.stackexchange.com/2.3"

@app.route('/search')
def search_question():
    query = request.args.get('query')
    url = f"{BASE_URL}/search?order=desc&sort=activity&intitle={query}&site=stackoverflow"
    res = requests.get(url)
    data = res.json()

    questions = []
    for item in data['items']:
        questions.append({
            'title': item['title'],
            'link': item['link'],
            'is_answered': item['is_answered']
        })

    csv_file = 'questions.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'is_answered'])
        writer.writeheader()
        writer.writerows(questions)

    return jsonify({'message': 'CSV file created', 'file': csv_file, 'total_questions': len(questions)})
