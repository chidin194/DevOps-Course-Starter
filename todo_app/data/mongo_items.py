import os
from bson import ObjectId
import pymongo

from todo_app.item import Item

def get_collection():

  client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

  db = client[os.getenv("MONGODB_DB_NAME")]

  collection = db[os.getenv("MONGODB_COLLECTION_NAME")]

  return collection


def get_items():
    collection = get_collection()

    documents = list(collection.find())

    items = []

    for document in documents:
        item = Item.from_mongo_document(document)
        items.append(item)

    return items


def add_item(title: str):
    collection = get_collection()

    new_item = {
        "status": "To Do", 
        "title": title
    }

    collection.insert_one(new_item)

def start_item(item_id: str):
    collection = get_collection()

    collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"status": "Doing"}})


def complete_item(item_id: str):
    collection = get_collection

    collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"status": "Done"}})


def delete_item(item_id: str):
    collection = get_collection()

    collection.delete_one({"_id": ObjectId(item_id)})