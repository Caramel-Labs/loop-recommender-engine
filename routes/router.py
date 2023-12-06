from fastapi import APIRouter
from bson import ObjectId
from db.config import remote_mongodb
from db.schemas import (
    event_individual_serial,
    event_list_serial,
    user_individual_serial,
    user_list_serial,
)
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

router = APIRouter()

# setup database
db = remote_mongodb()

# get collections from database
users_collection = db.get_collection("users")
events_collection = db.get_collection("events")


# root
@router.get("/", tags=["ROOT"])
async def root() -> dict:
    return {"message": "Hello World!"}


# check engine functionality (not necessary)
@router.get("/engine/")
async def engine() -> dict:
    return {"message": "Hello from the Recommender engine!"}


# get all users from database
@router.get("/users/")
async def get_users():
    global users_collection
    users = user_list_serial(users_collection.find())
    return users


# get all events from database
@router.get("/events/")
async def get_users():
    global events_collection
    events = event_list_serial(events_collection.find())
    return events


# handle liking and bookmarking events
@router.put("/like-event/{user_id}/{event_id}/")
@router.put("/bookmark-event/{user_id}/{event_id}/")
@router.get("/like-event/{user_id}/{event_id}/")
@router.get("/bookmark-event/{user_id}/{event_id}/")
async def like_or_bookmark_event(user_id: str, event_id: str):
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


# get recommendations for user
@router.get("/get-recommendations/{user_id}/")
async def get_recommendations(user_id):
    global users_collection
    global events_collection

    # get user from database
    user = user_individual_serial(users_collection.find_one({"username": user_id}))
    first_name = user["firstName"]
    interests = user["interests"]
    print(f"{first_name}'s interests: {interests}")

    # get events from database
    events = list(events_collection.find({}, {"_id": 1, "hashtags": 1}))
    print(f"Events: {events}")

    # extract hashtags for each event
    event_hashtags = [event["hashtags"] for event in events]

    # calculate cosine similarity scores
    scores = []
    user_interests = np.array(interests).reshape(1, -1)
    for event_tags in event_hashtags:
        event_tags = np.array(event_tags).reshape(1, -1)
        score = cosine_similarity(user_interests, event_tags)
        scores.append(score[0][0])

    # get top event indices based on scores
    number_of_recommendations = 5
    top_5_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
        :number_of_recommendations
    ]

    # get IDs of recommended events
    recommended_event_ids = [str(events[i]["_id"]) for i in top_5_indices]
    print(f"Recommended Event IDs: {recommended_event_ids}")

    # get array of recommended events
    recommended_events = [
        {
            "_id": str(events[i]["_id"]),
            "name": events[i].get("name"),
            "society": events[i].get("society"),
            "date": events[i].get("date"),
            "hashtags": events[i].get("hashtags"),
        }
        for i in top_5_indices
    ]
    print(f"Recommended Events: {recommended_events}")

    return {
        "message": "Recommendations calculated",
        "recommendations": recommended_events,
    }
