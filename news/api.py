from django.conf import settings
import requests

def fetch_news(query='뉴스', page_size=20):
    """
    NewsAPI를 호출하여 뉴스를 가져오는 공통 함수
    :param query: 검색할 쿼리
    :param page_size: 가져올 기사 수
    :return: (기사 리스트, 에러 메시지) 튜플
    """
    api_key = settings.NEWS_API_KEY
    url = 'https://newsapi.org/v2/everything'
    
    params = {
        'apiKey': api_key,
        'q': query,
        'sortBy': 'popularity',
        'language': 'ko',
        'pageSize': page_size
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok':
            return data.get('articles', []), None
        else:
            import json
            return [], f"API Error: {json.dumps(data, indent=2)}"
            
    except requests.exceptions.RequestException as e:
        return [], f"Network Error: {str(e)}"
    except Exception as e:
        return [], f"An unknown error occurred: {str(e)}"
