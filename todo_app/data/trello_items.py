import os
from todo_app.data.helpers import map_list_id_to_status
from todo_app.item import Item
from todo_app.trello_api import TrelloApi
def get_items():
    trello_api = TrelloApi(os.getenv('TRELLO_API_BASE_URL'), os.getenv('TRELLO_BOARD_ID'), os.getenv('TRELLO_API_TOKEN'), os.getenv('TRELLO_API_KEY'))
    board_lists = trello_api.get_cards()
    items = []

    for list in board_lists:
        for card in list['cards']:
            item = Item.from_trello_card(card.get('id'), map_list_id_to_status(card.get('idList')), card.get('name'))
            items.append(item)

    return items


def add_item(title):
    trello_api = TrelloApi(os.getenv('TRELLO_API_BASE_URL'), os.getenv('TRELLO_BOARD_ID'), os.getenv('TRELLO_API_TOKEN'), os.getenv('TRELLO_API_KEY'))
    new_item = trello_api.add_card(title)

    return {'id': new_item.get('id'), 'status': 'To Do', 'title': new_item.get('name')}


def complete_item(item_id):
    trello_api = TrelloApi(os.getenv('TRELLO_API_BASE_URL'), os.getenv('TRELLO_BOARD_ID'), os.getenv('TRELLO_API_TOKEN'), os.getenv('TRELLO_API_KEY'))
    trello_api.update_card(item_id, os.getenv('DONE_LIST_ID'))


def delete_item(item_id):
    trello_api = TrelloApi(os.getenv('TRELLO_API_BASE_URL'), os.getenv('TRELLO_BOARD_ID'), os.getenv('TRELLO_API_TOKEN'), os.getenv('TRELLO_API_KEY'))
    trello_api.delete_card(item_id)
