from profile import Profile
from bson import ObjectId
from fastapi import FastAPI
from db.config import remote_mongodb
from db.schemas import (
    event_individual_serial,
    event_list_serial,
    user_individual_serial,
    user_list_serial,
)

# instantiate FastAPI app
app = FastAPI()

# setup database
db = remote_mongodb()

# get collections from database
users_collection = db.get_collection("users")
events_collection = db.get_collection("events")


@app.get("/", tags=["ROOT"])
async def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/engine/")
async def engine() -> dict:
    return {"message": "Hello from the Recommender engine!"}


@app.get("/users/")
async def get_users():
    global users_collection
    users = user_list_serial(users_collection.find())
    return users


@app.get("/like-event/{user_id}/{event_id}/")
async def like_event(user_id: str, event_id: str):
    global users_collection
    global events_collection

    # get user from database
    user = user_individual_serial(users_collection.find_one({"username": user_id}))
    first_name = user["firstName"]
    interests = user["interests"]
    print(f"{first_name}'s interests: {interests}")

    # get event from database
    event = event_individual_serial(
        events_collection.find_one({"_id": ObjectId(event_id)})
    )
    event_name = event["name"]
    hashtags = event["hashtags"]
    print(f"{event_name}'s hashtags: {hashtags}")

    # some more code
    return {"message": "Like event handled"}
