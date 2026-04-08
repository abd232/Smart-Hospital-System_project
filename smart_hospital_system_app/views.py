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

def doctors(request):
    # Fetch doctor data from the database and pass it to the template
    doctors = []  # Replace with actual doctor data
    return render(request, 'doctors.html', {'doctors': doctors})

def ai(request):
    # Implement AI-related logic here
    return render(request, 'ai.html')

def book(request):
    if request.method == 'POST':
        # Handle booking logic here
        pass
    return render(request, 'booking.html')