# Schemas for users


def user_individual_serial(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstName": user["firstName"],
        "username": user["username"],
        "lastName": user["lastName"],
        "interests": user["interests"],
    }


def user_list_serial(users) -> list:
    return (user_individual_serial(user) for user in users)


# Schemas for events


def event_individual_serial(event) -> dict:
    return {
        "id": str(event["_id"]),
        "name": event["name"],
        "society": event["society"],
        "date": event["date"],
        "hashtags": event["hashtags"],
    }


def event_list_serial(events) -> list:
    return (user_individual_serial(event) for event in events)
