from django.shortcuts import render
from .api import fetch_news

def news_page(request):
    articles, error = fetch_news(page_size=21)
    
    context = {
        'articles': articles,
        'error': error,
    }
    return render(request, 'news/news_page.html', context)

