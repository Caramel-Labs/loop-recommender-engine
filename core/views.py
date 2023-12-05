from django.shortcuts import render, HttpResponse


def index(request):
    print("index() function of core app fired")
    return HttpResponse(request, "Hello world from the core app!")
