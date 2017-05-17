from django.http.response import HttpResponse
from django.shortcuts import render


def telegram_webhook(request):
    return HttpResponse(b"hello world!")
