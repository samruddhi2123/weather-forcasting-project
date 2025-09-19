import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CityForm
from .models import CitySearch

API_KEY = "aafd854f1ed3d844e43b334a6a6b7c4d"  # 🔑 get it from https://openweathermap.org/api

@login_required
def weather_view(request):
    weather_data = None
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url).json()
            if response.get("cod") == 200:
                temp = response['main']['temp']
                humidity = response['main']['humidity']
                wind = response['wind']['speed']

                CitySearch.objects.create(
                    user=request.user,
                    city=city,
                    temperature=temp,
                    humidity=humidity,
                    wind_speed=wind
                )
                weather_data = {
                    'city': city,
                    'temperature': temp,
                    'humidity': humidity,
                    'wind': wind
                }
    else:
        form = CityForm()

    history = CitySearch.objects.filter(user=request.user).order_by('-searched_at')[:5]
    return render(request, "weather_app/weather.html", {"form": form, "weather": weather_data, "history": history})

from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "weather_app/signup.html", {"form": form})

# Create your views here.
