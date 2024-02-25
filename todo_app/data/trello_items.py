import os
from todo_app.data.helpers import map_list_id_to_status
from todo_app.item import Item
from todo_app.trello_api import TrelloApi

def get_items():
    board_lists = TrelloApi.get_cards()
    items = []

    for list in board_lists:
        for card in list['cards']:
            item = Item.from_trello_card(card.get('id'), map_list_id_to_status(card.get('idList')), card.get('name'))
            items.append(item)

    return items


def add_item(title):
    new_item = TrelloApi.add_card(title)
    return {'id': new_item.get('id'), 'status': 'To Do', 'title': title}


def complete_item(item_id):
    TrelloApi.update_card(item_id, os.getenv('DONE_LIST_ID'))


def delete_item(item_id):
    TrelloApi.delete_card(item_id)
