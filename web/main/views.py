from django.http.response import HttpResponse
from django.shortcuts import render


def telegram_webhook(request):
    return HttpResponse(b"hello world!")


def main(request):
    return HttpResponse(b"Hi, this is main page")
