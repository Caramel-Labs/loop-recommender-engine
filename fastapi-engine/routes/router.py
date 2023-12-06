from fastapi import APIRouter
from bson import ObjectId
from db.config import remote_mongodb
from db.schemas import (
    event_individual_serial,
    event_list_serial,
    user_individual_serial,
    user_list_serial,
)

router = APIRouter()

# setup database
db = remote_mongodb()

# get collections from database
users_collection = db.get_collection("users")
events_collection = db.get_collection("events")


@router.get("/", tags=["ROOT"])
async def root() -> dict:
    return {"message": "Hello World!"}


@router.get("/engine/")
async def engine() -> dict:
    return {"message": "Hello from the Recommender engine!"}


@router.get("/users/")
async def get_users():
    global users_collection
    users = user_list_serial(users_collection.find())
    return users


@router.get("/events/")
async def get_users():
    global events_collection
    events = event_list_serial(events_collection.find())
    return events


@router.get("/like-event/{user_id}/{event_id}/")
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

    # update list of user's interests
    interests = update_user_interests(
        interests=interests,
        hashtags=hashtags,
    )

    print(f"{first_name}'s new interests: {interests}")

    # write new interests to database
    users_collection.update_one(
        {"username": user_id},
        {
            "$set": {"interests": interests},
        },
    )

    return {"message": "Like event handled"}


def update_user_interests(interests, hashtags: list) -> list:
    # get hashtags that are not in user's interests
    missing_interests = set(hashtags) - set(interests)
    print(missing_interests)

    # add missing hashtags to user's interests
    interests.extend(list(missing_interests))

    # remove old interests if too many interests are present
    interest_cap = 20
    if len(interests) > interest_cap:
        print("Too many interests")
        interests = interests[-20:]
    else:
        print("Less than 20 interests are available")

    return interests
