from django.shortcuts import render
from .models import Product

def market_page(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'market/market_page.html', context)