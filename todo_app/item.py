class Item:
    def __init__(self, id, status, title):
        self.id = id
        self.status = status
        self.title = title


    @classmethod
    def from_mongo_document(cls, document):
        return cls(document['_id'], document['status'], document['title'])