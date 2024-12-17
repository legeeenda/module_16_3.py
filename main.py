from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI()

users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}



class UserInput(BaseModel):
    username: str = Field(..., min_length=1, description="Имя пользователя")
    age: int = Field(..., ge=0, le=120, description="Возраст пользователя")



@app.get("/users", summary="Получить всех пользователей")
async def get_users() -> Dict[str, str]:
    return users



@app.post("/user/{username}/{age}", summary="Добавить нового пользователя")
async def add_user(username: str, age: int):

    max_key = max(map(int, users.keys()), default=0)
    new_key = str(max_key + 1)
    users[new_key] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_key} is registered"}



@app.put("/user/{user_id}/{username}/{age}", summary="Обновить данные пользователя")
async def update_user(user_id: str, username: str, age: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {user_id} has been updated"}



@app.delete("/user/{user_id}", summary="Удалить пользователя")
async def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    del users[user_id]
    return {"message": f"User {user_id} has been deleted"}
