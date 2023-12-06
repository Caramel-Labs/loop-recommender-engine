def individual_serial(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstName": user["firstName"],
        "lastName": user["lastName"],
    }


def list_serial(users) -> list:
    return (individual_serial(user) for user in users)
