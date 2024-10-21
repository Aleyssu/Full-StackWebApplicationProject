import pytest
from app import app  # Assuming your Flask app is in `app.py`

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms if needed
    with app.test_client() as client:
        yield client