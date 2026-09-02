from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pymongo import MongoClient
from models.todo import Todo, Update_todo
from dotenv import load_dotenv
import os

from bson import ObjectId

#loading .env
load_dotenv()

#FastApi app
app = FastAPI()


# mongodb setup
client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=5000)
collection = client['Todo']['todos']

# --- Rate limiter setup ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# get Todos
@app.get('/todos')
@limiter.limit("100/minute")
def get_todo(request : Request):
    try:
        data = list(collection.find())
        for todo in data:
            todo["_id"] = str(todo["_id"])
    except Exception as e:
         raise HTTPException(status_code=500)
    return {"todos": len(data),"result":data}

@app.get("/todo/{todo_id}")
@limiter.limit("100/minute")
def get_todo_by_id(request: Request, todo_id: str):
    try:
        data = collection.find_one({"_id": ObjectId(todo_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")

    data["_id"] = str(data["_id"])
    return {"result": data}


@app.post('/add-todo')
@limiter.limit("100/minute")
def add_todo(request : Request, todo : Todo):
    try:
        result = collection.insert_one(todo.model_dump())
    except Exception :
        raise HTTPException(status_code = 400,detail="Enter Valid Input")
    return {
        "todo": todo.model_dump(),
        "id": str(result.inserted_id)
    }

@app.put("/update-todo")
@limiter.limit("100/minute")
def update_data(request : Request, todo_id : str, update_todo : Update_todo):
    try:
        result = collection.update_one(
            {"_id" : ObjectId(todo_id)},
            {"$set" : update_todo.model_dump()}
            )
    except Exception:
        raise HTTPException(status_code = 400, detail="Invalid Todo ID")
    
    if result.matched_count == 0:
        raise HTTPException(status_code = 404, detail="Item not found")
    
    return {"todo_id" : todo_id, "Todo" : update_todo.model_dump()}


@app.delete("/todo-delete/{todo_id}")
@limiter.limit("100/minute")
def del_todo(request : Request, todo_id : str):
    try:
        result = collection.delete_one({"_id": ObjectId(todo_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": "deleted", "id": todo_id}