from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

user_db = {
    1: {"name": "John", "age": 30},
    2: {"name": "Smith", "age": 25},
    3: {"name": "Alice", "age": 28},
}

@app.get("/sudhanshu/kumar/xyz")
def add(a: int, b: int):
    return a + b

class subtractmodel(BaseModel):
    a: int
    b: int


def subtract(a: int, b: int):
    return a - b

@app.post("/subtract")
def subtract_number(model: subtractmodel):
    return subtract(model.a, model.b)

class User(BaseModel):
    name:str
    age:int

#PUT: to update the data, eg. into DB
@app.put("/user_db/date/v1/update/{user_id}")
def user_update(user_id:int, user:User):
    if user_id in user_db:
        user_db[user_id] = user.dict()
        print(user_db)
        return {"message": "User updated successfully", "user": user}
    else:
        return {"message": "User not found"}

#DELETE: to delete the data, eg. from DB
@app.delete("/user_db/date/v1/delete/{user_id}")
def delete_user(user_id:int):
    if user_id in user_db:
        del user_db[user_id]
        print(user_db)
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}