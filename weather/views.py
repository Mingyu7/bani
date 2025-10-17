from django.shortcuts import render

def weather_page(request):
    return render(request, 'weather/weather_page.html')