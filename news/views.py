from django.shortcuts import render

def news_page(request):
    return render(request, 'news/news_page.html')
