from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def ask(request):
    return render(request, 'main/ask.html')

def question(request):
    return render(request, 'main/question.html')

def login(request):
    return render(request, 'main/login.html')

def signup(request):
    return render(request, 'main/signup.html')

def settings(request):
    return render(request, 'main/settings.html')
