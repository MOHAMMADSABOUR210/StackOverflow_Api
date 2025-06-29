# StackOverflow Question Fetcher API

This Flask-based API fetches and optionally stores StackOverflow questions based on user queries or tags using the [StackExchange API](https://api.stackexchange.com/).

## Features

- **Search Questions by Title**  
  Fetches questions matching a keyword in the title.

- **Filter Questions by Tag**  
  Fetches recent questions filtered by a specific tag.

- **Get Detailed Questions by Tag and Count**  
  Returns detailed questions for a tag with body and metadata. Allows limiting the number of returned items.

- **Optional Database Saving**  
  Supports saving fetched questions to a database using SQLAlchemy models (`Question`, `SearchQuestion`, `Tags`).

## Endpoints

### `GET /search`
Search StackOverflow questions by title.  
**Query Parameters**:
- `query`: (required) The search keyword.
- `save`: (optional, default `false`) Whether to save results to the database.

### `GET /tags/<tag>`
Fetches recent questions with a specific tag.  
**Query Parameters**:
- `save`: (optional, default `false`) Whether to save results to the database.

### `GET /tag-questions/<tag>`
Returns detailed questions by tag.  
**Query Parameters**:
- `count`: (optional, default `1`) Number of questions to return.
- `save`: (optional, default `false`) Whether to save results to the database.

## Requirements

- Python 3.x  
- Flask  
- SQLAlchemy  
- requests

## Usage

Start the Flask server:
```bash
flask run
```

Example request:
```bash
curl "http://localhost:5000/search?query=flask&save=true"
```

## Database Models

The API uses three SQLAlchemy models to store different types of data retrieved from StackOverflow:

### `Question`
Stores detailed information about individual questions fetched by tag, including full body content.

**Fields**:
- `question_id` *(Integer, Primary Key)* – Unique ID of the question.
- `title` *(String)* – Title of the question.
- `link` *(String)* – URL to the question on StackOverflow.
- `tags` *(String)* – Comma-separated tags.
- `is_answered` *(Boolean)* – Whether the question has an accepted answer.
- `score` *(Integer)* – Score (upvotes - downvotes).
- `creation_date` *(Integer or DateTime)* – UNIX timestamp of when the question was created.
- `body` *(Text)* – Full HTML body of the question.

### `SearchQuestion`
Stores lightweight search results without full body content.

**Fields**:
- `id` *(Integer, Primary Key)* – Auto-incremented ID.
- `title` *(String)* – Title of the question.
- `link` *(String)* – URL to the question.
- `is_answered` *(Boolean)* – Whether the question has an accepted answer.

### `Tags`
Stores questions filtered by a specific tag.

**Fields**:
- `id` *(Integer, Primary Key)* – Auto-incremented ID.
- `tags` *(String)* – Tag used for filtering.
- `title` *(String)* – Question title.
- `link` *(String)* – URL to the question.
- `owner` *(String)* – Display name of the question’s owner.
- `is_answered` *(Boolean)* – Whether the question has an accepted answer.
- `view_count` *(Integer)* – Number of views.
- `answer_count` *(Integer)* – Number of answers.
- `score` *(Integer)* – Score of the question.

## Database Initialization

Before using the API, make sure the database is initialized:

```python
from models import db
db.create_all()
```

Ensure that your Flask app is properly configured with a valid `SQLALCHEMY_DATABASE_URI` and that you have called `db.init_app(app)` in your `models.py`.