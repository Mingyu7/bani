from django.shortcuts import render

def map_page(request):
    return render(request, 'map/map_page.html')