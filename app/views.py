from django.shortcuts import render
from json import JSONDecoder
from django.http import JsonResponse

def test(request):
  return JsonResponse({"message": "Hello World"})

# def generate(request):
