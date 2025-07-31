from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    nome: str
    email: str

db: List[User] = []

@app.get("/")
def read_root():
    return {"message": "API funcionando!"}

@app.post("/users")
def create_user(user: User):
    db.append(user)
    return user

@app.get("/users")
def list_users():
    return db
