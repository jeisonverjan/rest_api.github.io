import json
from typing import List
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from random import randint

class User(BaseModel):
    name: str
    country: str
    category: str
    born: str
    live: bool
    photo: str
    gender: str
    tags: List

app = FastAPI(
    title="Thousand celebrities - API.",
    description="In this API you can obtain information about thousands of celebrities of all times in different categories. You can nominate a new celebrity, which after verification will be added; additionally, you can request to update or modify information of existing celebrities.",
    docs_url="/"
    
)

with open("celebrities.json", "r") as f:
    data = json.load(f)

index = len(data)

categories = {}
for i in data:
    category = data[i]['category']
    if category in categories.keys():
        categories[category] += 1
    else:
        categories[category] = 1

@app.get('/home', tags=['Get data'])
async def home():
    return data

@app.get('/categories', tags=['Get data'])
async def home():
    return categories

@app.get("/limit/{number}", tags=['Get data'])
async def get_user_by_limit(number: int = Path(None, description="Get random celebrities, enter the number of records you want.", gt=0, lt=index+1)):
    data_limit = {}
    while len(data_limit) < number:
        random_num = str(randint(1, len(data)))
        data_limit[random_num] = data[random_num]
    return data_limit

@app.get("/get-user/{user_id}", tags=['Get data'])
async def get_user_by_id(user_id: int = Path(None, description="Get a celebrity by ID, enter the ID you want to get.", gt=0, lt=index+1)):
    global index
    if str(user_id) not in data.keys():
        raise HTTPException(status_code=400, detail="User not found.")

    return data[str(user_id)]

@app.get("/get-user-name/{user_name}", tags=['Get data'])
async def get_user_by_name(user_name: str = Path(None, description="Get a celebrity by name, enter the name or part of the name, return a dictionary with the matches found.")):
    user_by_name = {}
    for i in data:
        for j in i:
            celebrity_name = data[i]['name'].lower()
            if celebrity_name.__contains__(user_name.lower()):
                user_by_name[i] = data[i]
    if len(user_by_name) == 0:
        raise HTTPException(status_code=400, detail="User not found.")        
    else:
        return user_by_name


@app.post("/create-celebrity", tags=['Add new celebrity request'])
async def create_celebrity(user: User):
    file_name = "celebrities_requests.json"
    celebrity_request = {"name": user.name, "country": user.country, "category":user.category, "born": user.born, "live":user.live, "photo":user.photo, "gender":user.gender, "tags": user.tags}
    with open(file_name, "r") as file:
        info = json.load(file)
    cont_file = len(info)
    info[str(cont_file)] = celebrity_request
    with open(file_name, "w") as file:
        json.dump(info, file)

    return "Your request has been received, after verification the celebrity will be added.", info[str(cont_file)]

@app.get('/celebrity-request', tags=['Add new celebrity request'])
async def celebrities_requests():
    with open("celebrities_requests.json", "r") as file:
        data = json.load(file)
    return data


@app.post("/celebrity-update/{user_id}", tags=['Celebrity Update request'])
async def celebrity_update(user: User, user_id: int = Path(None, description="Enter the ID you want to modify and fill the fileds to update.", gt=0)):
    global index
    if str(user_id) not in data.keys():
        raise HTTPException(status_code=400, detail="User not found.")
    file_name = "celebrities_update.json"
    celebrity_update = {"name": user.name, "country": user.country, "category":user.category, "born": user.born, "live":user.live, "photo":user.photo, "gender":user.gender, "tags": user.tags}
    with open(file_name, "r") as file:
        info = json.load(file)
    info[str(user_id)] = celebrity_update
    with open(file_name, "w") as file:
        json.dump(info, file)

    return "Your request has been received, after verification the celebrity will be updated.", info[str(user_id)]


@app.get('/update-requests', tags=['Celebrity Update request'])
async def update_requests():
    with open("celebrities_update.json", "r") as file:
        data = json.load(file)
    return data