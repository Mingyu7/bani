from django.shortcuts import render

def weather_page(request):
    cities = [
        ('Seoul', '서울특별시'), ('Busan', '부산'), ('Daegu', '대구'), ('Incheon', '인천'),
        ('Gwangju', '광주'), ('Daejeon', '대전'), ('Ulsan', '울산'), ('Jeju', '제주'),
        ('Suwon', '수원'), ('Chuncheon', '춘천'), ('Cheongju', '청주'), ('Cheonan', '천안'),
        ('Jeonju', '전주'), ('Mokpo', '목포'), ('Pohang', '포항'), ('Changwon', '창원')
    ]
    context = {'cities': cities}
    return render(request, 'weather/weather_page.html', context)