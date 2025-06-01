from flask import Flask, request, jsonify
import requests
import csv  
import os  

app = Flask(__name__)
BASE_URL = "https://api.stackexchange.com/2.3"

@app.route('/search')
def search_question():
    query = request.args.get('query')
    save_csv = request.args.get('save', 'false').lower() == 'true'

    if not query:
        return jsonify({'error': 'Missing "query" parameter'}), 400

    try:
        url = f"{BASE_URL}/search?order=desc&sort=activity&intitle={query}&site=stackoverflow"
        res = requests.get(url)
        res.raise_for_status()  # raises error if bad HTTP status

        data = res.json()
        items = data.get('items', [])

        if not items:
            return jsonify({'message': 'No questions found'}), 404

        questions = [{
            'title': item.get('title'),
            'link': item.get('link'),
            'is_answered': item.get('is_answered')
        } for item in items]

        if save_csv:
            csv_file = 'questions.csv'
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'link', 'is_answered'])
                writer.writeheader()
                writer.writerows(questions)

        return jsonify(questions)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch from StackExchange', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/tags/<tag>')
def filter_by_tag(tag):
    url = f"{BASE_URL}/questions?order=desc&sort=activity&tagged={tag}&site=stackoverflow"
    res = requests.get(url)

    save_tag = request.args.get('save_tag', 'false').lower() == 'true'
    
    data = res.json()
    items = data['items']


    if not items:
        return jsonify({'message': 'No questions found'}), 404

    fieldnames = list(items[0].keys())

    processed_items = []
    for item in items:
        flat_item = {}
        for key in fieldnames:
            value = item.get(key)
            if isinstance(value, (dict, list)):
                flat_item[key] = str(value)
            else:
                flat_item[key] = value
        processed_items.append(flat_item)

    if save_tag:
        csv_file = r'save_tag.csv'
        
        print("Current Working Directory:", os.getcwd())

        try:
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_items)
        except Exception as e:
            return jsonify({'error': 'Failed to save CSV', 'details': str(e)}), 500
        
        return jsonify({'message': 'CSV file saved', 'file': csv_file, 'total_questions': len(processed_items)})


    return jsonify(data)
