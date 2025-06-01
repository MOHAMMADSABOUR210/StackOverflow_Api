from flask import  request, jsonify
from models import Question ,SearchQuestion , Tags, app, db

import requests
# 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    tags = db.Column(db.String)
    is_answered = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    creation_date = db.Column(db.Integer)
    body = db.Column(db.Text)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    is_answered = db.Column(db.Boolean)
    view_count = db.Column(db.Integer)
    answer_count = db.Column(db.Integer)
    score = db.Column(db.Integer)

class SearchQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    is_answered = db.Column(db.Boolean)


# 

BASE_URL = "https://api.stackexchange.com/2.3"

@app.route('/search')
def search_question():
    query = request.args.get('query')
    save_db = request.args.get('save_db', 'false').lower() == 'true'

    if not query:
        return jsonify({'error': 'Missing "query" parameter'}), 400

    try:
        url = f"{BASE_URL}/search?order=desc&sort=activity&intitle={query}&site=stackoverflow"
        res = requests.get(url)
        res.raise_for_status()

        data = res.json()
        items = data.get('items', [])

        if not items:
            return jsonify({'message': 'No questions found'}), 404

        questions = []
        for item in items:
            q = {
                'title': item.get('title'),
                'link': item.get('link'),
                'is_answered': item.get('is_answered')
            }
            questions.append(q)

            if save_db:
                question_obj = SearchQuestion(title=q['title'],
                                               link=q['link'], 
                                               is_answered=q['is_answered'])
                db.session.add(question_obj)


        if save_db:
            db.session.commit()

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
        for item in items:
            tag_entry = Tags(
                tags=tag,
                title=item.get('title'),
                link=item.get('link'),
                owner=item.get('owner', {}).get('display_name', 'Unknown'),
                is_answered=item.get('is_answered'),
                view_count=item.get('view_count'),
                answer_count=item.get('answer_count'),
                score=item.get('score')
            )
            db.session.add(tag_entry)
        db.session.commit()

        return jsonify({'message': 'Tags saved to database', 'total_questions': len(processed_items)})


    return jsonify(data)



@app.route('/tag-questions/<tag>')
def get_questions_by_tag(tag):
    count = int(request.args.get('count', 1))
    save = request.args.get('save', 'false').lower() == 'true'

    url = f"{BASE_URL}/questions?order=desc&sort=activity&tagged={tag}&site=stackoverflow"
    res = requests.get(url)
    data = res.json()

    items = data.get('items', [])
    if not items:
        return jsonify({'message': 'No questions found'}), 404
    print(count)
    if count >= 0:
        selected_questions = items[:count]
    else :
        return jsonify({'message': 'The number entered is not correct'}), 404

    question_ids = [str(q['question_id']) for q in selected_questions]

    detail_url = f"https://api.stackexchange.com/2.3/questions/{';'.join(question_ids)}?order=desc&sort=activity&site=stackoverflow&filter=withbody"
    detail_res = requests.get(detail_url)
    detail_data = detail_res.json()
    details = detail_data.get('items', [])

    if save:
        for q in details:
            existing = Question.query.filter_by(question_id=q['question_id']).first()
            if existing:
                continue
            question = Question(
                question_id=q['question_id'],
                title=q['title'],
                link=q['link'],
                tags=','.join(q['tags']),
                is_answered=q['is_answered'],
                score=q['score'],
                creation_date=q['creation_date'],
                body=q['body']
            )
            db.session.add(question)
        db.session.commit() 

        return jsonify({'message': 'Questions saved to database', 'total_saved': len(details)})

    return jsonify({'questions': details})