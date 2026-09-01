from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

from bson import ObjectId

#loading .env
load_dotenv()

#FastApi app
app = FastAPI()


# mongodb setup
client = MongoClient(os.getenv('MONGODB_URI'))
collection = client['Todo']['todos']


# get Todos
@app.get('/todos')
def get_todo():
    data = list(collection.find())
    for todo in data:
        todo["_id"] = str(todo["_id"])
    return {"todos": collection.count_documents({}),"result":data}

@app.get("/todos/{todo_id}")
def get_todo(todo_id : str):
    data = collection.find_one({"_id":ObjectId(todo_id)})
    if data is None:
        return {"message": "Todo not found"}

    data["_id"] = str(data["_id"])
    return {"data" : data}

