# Requirement
pip install Flask-SQLAlchemy Werkzeug
pip install pytest flask-testing requests

# Archi
tree -I '__pycache__|venv|env'
├── app
│	├── database.py
│	├── __init__.py
│	├── models
│	│	├── __init__.py
│	│	├── table.py
│	│	└── user.py
│	└── routes
│	    ├── __init__.py
│	    ├── table.py
│	    └── user.py
├── config.py
├── instance
│	└── test.db
├── readme.txt
├── run.py
└── tests
    └── test_user.py

# TEST
export PYTHONPATH=$(pwd)
pytest
