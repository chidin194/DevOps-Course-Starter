import os
from dotenv import load_dotenv, find_dotenv
import pytest
import requests
from todo_app import app
from todo_app.tests.StubResponse import StubResponse
from unittest.mock import MagicMock

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub_get_lists)

    response = client.get('/')
    
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()


def test_add_new_to_do(monkeypatch, client):
    stub_create_to_do = MagicMock()
    monkeypatch.setattr(requests, 'post', stub_create_to_do)

    response = client.post('/', follow_redirects=True)

    assert response.status_code == 200
    assert 'To-Do App' in response.data.decode()
    stub_create_to_do.assert_called_once_with('https://api.trello.com/1/cards', 
        data={'key': 'test_trello_api_key', 'token': 'test_trello_api_token', 'name': None, 'idList': 'test_to_do_list_id'})
    

def stub_get_lists(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card', 'idList': '123abc'},]
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')

def stub_create_to_do(url, data={}):
    fake_response_data = None

    if url == 'https://api.trello.com/1/cards':
        fake_response_data = {
            'id': '123abc',
            'idBoard': os.environ.get('TRELLO_BOARD_ID'),
            'idList': os.environ.get('TO_DO_LIST_ID'),
            'name': 'New test to-do'}
        return StubResponse(fake_response_data)