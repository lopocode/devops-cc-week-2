import pytest
from app import app  # replace with the name of your Python file containing the Flask app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "healthy"

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'index.html' in response.data  # Update this assertion based on your index.html content

@patch('requests.get')
def test_quote_route(mock_get, client):
    mock_get.return_value.text = "Mock Quote"
    response = client.get('/get_quote')
    assert response.status_code == 200
    mock_get.assert_called_once_with("http://quote-gen-container:5000/quote")
    assert b'quote.html' in response.data  # Update this assertion based on your quote.html content
    assert b'Mock Quote' in response.data
