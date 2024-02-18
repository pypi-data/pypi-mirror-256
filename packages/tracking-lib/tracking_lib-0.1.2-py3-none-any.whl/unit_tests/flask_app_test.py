import sys
sys.path.append("..")

from flask import Flask, jsonify
import pytest
from src.transaction import Transaction

app = Flask(__name__)

def interactor_runc():
    #print(f"transaction_id in interactor func: {Transaction.read_transaction_id()}")
    return Transaction.read_transaction_id()

@app.route('/')
def hello_world():
    Transaction.set_transaction_id("123456")
    tr_id = interactor_runc()
    return jsonify(message=tr_id)

# Test client fixture
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Unit test
def test_hello_world(client):
    response = client.get('/')
    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == "123456"
