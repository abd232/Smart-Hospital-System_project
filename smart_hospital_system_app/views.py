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

<<<<<<< HEAD
def doctors(request):
    # Fetch doctors from the database and pass them to the
    # template for rendering
    return render(request, 'doctors.html')
=======
def ai(request):
    return render(request, 'Ai.html')
>>>>>>> 9e38d55 (Adding ai page)
