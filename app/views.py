from django.shortcuts import render
from json import JSONDecoder
from django.views import View
from django.http import JsonResponse

def test(request):
  return JsonResponse({"message": "Hello World"})

# def index(request):
#     return render(request, 'app/templates/index.html')

def index(request, template="index.html"):
    return render(request, template, {})

# def generate(request):
