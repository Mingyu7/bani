// 날씨 위젯 스크립트
const WEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY';
const weatherWidget = document.getElementById('weather-widget');

if (weatherWidget) { // 위젯이 존재하는 경우에만 실행
    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${WEATHER_API_KEY}&units=metric&lang=kr`)
            .then(response => response.json())
            .then(data => {
                if (data.cod === 200) {
                    const icon = `https://openweathermap.org/img/wn/${data.weather[0].icon}.png`;
                    const temp = Math.round(data.main.temp);
                    const description = data.weather[0].description;
                    weatherWidget.innerHTML = `
                        <img src="${icon}" alt="날씨 아이콘" style="width: 50px; height: 50px; margin-right: 15px;">
                        <div>
                            <p class="mb-0 fs-5">${temp}°C</p>
                            <p class="mb-0 text-muted">${description}</p>
                        </div>
                    `;
                } else {
                    weatherWidget.innerHTML = `<p>날씨 정보를 가져올 수 없습니다.</p>`;
                }
            })
            .catch(() => {
                weatherWidget.innerHTML = `<p>날씨 정보를 불러오는 데 실패했습니다.</p>`;
            });
    }, () => {
        weatherWidget.innerHTML = `<p>위치 정보 사용을 허용해주세요.</p>`;
    });
}
