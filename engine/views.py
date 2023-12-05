from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Event


def index(request):
    print("index() function of recommender engine fired")
    return HttpResponse(request, "Hello world from the Recommender Engine!")


@csrf_exempt
def handle_like(request):
    print("Like handler fired")
    if request.method == "POST":
        # get user ID and event ID from request
        user_id = request.POST.get("user_id")
        event_id = request.POST.get("event_id")

        # update user interests
        update_user_interests(user_id, event_id)

        # return successful response
        return JsonResponse({"message": "Like handling completed."})


@csrf_exempt
def handle_bookmark(request):
    print("Bookmark handler fired")
    if request.method == "POST":
        # get user ID and event ID from request
        user_id = request.POST.get("user_id")
        event_id = request.POST.get("event_id")

        # update user interests
        update_user_interests(user_id, event_id)

        # return successful response
        return JsonResponse({"message": "Bookmark handling completed."})


def get_user_interests(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user.interests
        # if interests are comma separated values, use:
        # return user.interests.split(",")
    except User.DoesNotExist:
        return []


def get_event_hashtags(event_id):
    try:
        event = Event.objects.get(event_id=event_id)
        return event.hashtags
        # if hashtags are comma separated values, use:
        # return event.hashtags.split(",")
    except Event.DoesNotExist:
        return []


def update_user_interests(user_id, event_id):
    # get user's interests from db
    interests = get_user_interests(user_id=user_id)

    # get event hashtags from db
    event_hashtags = get_event_hashtags(event_id)

    # append event hashtags to user interests
    interests.extend(event_hashtags)

    # ensure maximum 20 elements in user interests
    if len(interests) > 20:
        interests = interests[-20:]  # Keep the last 20 elements

    updated_interests = interests

    # convert interests list back to a comma-separated string for database storage
    # updated_interests = ",".join(interests)

    # update user interests in the database
    try:
        user = User.objects.get(user_id=user_id)
        user.interests = updated_interests
        user.save()
    except User.DoesNotExist:
        # if user interests don't exist, create a new entry
        User.objects.create(user_id=user_id, interests=updated_interests)
