from django.shortcuts import render

def market_page(request):
    return render(request, 'market/market_page.html')