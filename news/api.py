import requests

def fetch_news(query='뉴스', page_size=20):
    """
    Naver News API를 호출하여 뉴스를 가져오는 공통 함수
    :param query: 검색할 쿼리
    :param page_size: 가져올 기사 수
    :return: (기사 리스트, 에러 메시지) 튜플
    """
    client_id = "071gfl6XcAM3lTJpqiFj"
    client_secret = "gYT57I2X4i"
    url = "https://openapi.naver.com/v1/search/news.json"
    
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    
    params = {
        'query': query,
        'display': page_size,
        'sort': 'sim',
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        return data.get('items', []), None
            
    except requests.exceptions.RequestException as e:
        return [], f"Network Error: {str(e)}"
    except Exception as e:
        return [], f"An unknown error occurred: {str(e)}"
