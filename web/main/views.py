from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def telegram_webhook(request):
    print("got 33smthing: {}".format(request.body))
    return HttpResponse(b"hello world!")


def main(request):
    return HttpResponse(b"Hi, this is main page")
