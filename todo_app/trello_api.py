import os
import requests

class TrelloApi:

  base_url = os.getenv('TRELLO_API_BASE_URL')
  board_id = os.getenv('TRELLO_BOARD_ID')
  token = os.getenv('TRELLO_API_TOKEN')
  key = os.getenv('TRELLO_API_KEY')

  @classmethod
  def get_cards(cls):
    url = f"{cls.base_url}/1/boards/{cls.board_id}/lists"

    params = {
        "key": cls.key,
        "token": cls.token,
        "cards": "open",
        "card_fields": "id,idList,name"
      }
    
    try:    
      response = requests.get(url, params=params)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      return None
    

  @classmethod
  def add_card(cls, title):
    url = f"{cls.base_url}/1/cards"

    data = {
      "key": cls.key,
      "token": cls.token,
      "name": title,
      "idList": os.getenv('TO_DO_LIST_ID')
    }

    try:    
      response = requests.post(url, data=data)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      return None
    

  @classmethod
  def update_card(cls, card_id, list_id):
    url = f"{cls.base_url}/1/cards/{card_id}"

    params = {
      "key": cls.key,
      "token": cls.token,
      "idList": list_id
    }
    
    try:    
      response = requests.put(url, params=params)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      return None
    

  @classmethod
  def delete_card(cls, card_id):
    url = f"{cls.base_url}/1/cards/{card_id}"

    params = {
      "key": cls.key,
      "token": cls.token,
    }

    try:    
      response = requests.delete(url, params=params)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      return None
  