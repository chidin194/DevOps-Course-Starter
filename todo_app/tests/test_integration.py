import os
from dotenv import load_dotenv, find_dotenv
import pytest
import mongomock
import pymongo
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    mongo_client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

    db = mongo_client[os.getenv("MONGODB_DB_NAME")]

    collection = db[os.getenv("MONGODB_COLLECTION_NAME")]
    
    test_document = {
        "title": "Test card",
        "status": "To Do"
    }

    collection.insert_one(test_document)

    response = client.get('/')
    
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()
