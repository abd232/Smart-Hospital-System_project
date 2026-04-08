from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'register.html')