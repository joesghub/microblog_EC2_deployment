import pytest
from microblog import app  # Import your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    # Send a GET request to the homepage
    response = client.get('/', follow_redirects=True)
    
    # Assert that the final response status code is 200 (OK)
    assert response.status_code == 200
