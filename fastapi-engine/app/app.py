from profile import Profile
from fastapi import FastAPI
from db.config import remote_mongodb
from db.schemas import list_serial

# instantiate FastAPI app
app = FastAPI()

# setup database
db = remote_mongodb()


@app.get("/", tags=["ROOT"])
async def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/engine/")
async def engine() -> dict:
    return {"message": "Hello from the Recommender engine!"}


@app.get("/users/")
async def get_users():
    users_collection = db.get_collection("users")
    users = list_serial(users_collection.find())
    return users
