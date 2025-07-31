
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

db: List[User] = []

@app.post("/users", response_model=User)
def create_user(user: User):
    db.append(user)
    return user

@app.get("/users", response_model=List[User])
def list_users():
    return db
