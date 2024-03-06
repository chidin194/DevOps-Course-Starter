class Item:
    def __init__(self, id, status, title):
        self.id = id
        self.status = status
        self.title = title


    @classmethod
    def from_trello_card(cls, card_id, card_name, list):
        return cls(card_id, card_name, list)