import os
import requests

class TrelloApi:

  def __init__(self, base_url, board_id, token, key):
    self.base_url = base_url
    self.board_id = board_id
    self.token = token
    self.key = key
    

  def get_cards(self):
    url = f"{self.base_url}/1/boards/{self.board_id}/lists"

    params = {
        "key": self.key,
        "token": self.token,
        "cards": "open",
        "card_fields": "id,idList,name"
      }
    
    try:    
      response = requests.get(url, params=params)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      return []
    

  def add_card(self, title):
    url = f"{self.base_url}/1/cards"

    data = {
      "key": self.key,
      "token": self.token,
      "name": title,
      "idList": os.getenv('TO_DO_LIST_ID')
    }

    try:    
      response = requests.post(url, data=data)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      raise
    

  def update_card(self, card_id, list_id):
    url = f"{self.base_url}/1/cards/{card_id}"

    params = {
      "key": self.key,
      "token": self.token,
      "idList": list_id
    }
    
    try:    
      response = requests.put(url, params=params)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      raise
    

  def delete_card(self, card_id):
    url = f"{self.base_url}/1/cards/{card_id}"

    params = {
      "key": self.key,
      "token": self.token,
    }

    try:    
      response = requests.delete(url, params=params)
      return response.json()
    except Exception as e:
      print(f"An error occurred: {e}")
      raise
  