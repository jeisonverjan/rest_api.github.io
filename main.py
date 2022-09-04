import json
from typing import List
from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel

class User(BaseModel):
    name: str
    country: str
    category: str
    born: str
    live: bool
    photo: str
    geder: str
    tags: List

app = FastAPI()

with open("celebrities.json", "r") as f:
    data = json.load(f)

index = len(data)

categories = {}
for index, categ in enumerate(data):
    if categ['category'] not in categories.values():
        categories[index] = categ['category']

@app.get('/')
def home():
    return data

@app.get('/categories')
def home():
    return categories

@app.get("/get-user/{user_id}")
def get_user(user_id: int = Path(None, description="From 0 to 5", gt=-1)):
    global index
    if user_id > index:
        raise HTTPException(status_code=400, detail="User not found.")

    return data[user_id]

@app.post("/create-user")
def create_user(user: User):
    global index
    data.append(user)
    index +=1
    return data[index]