document.addEventListener('DOMContentLoaded', function() {
    const apiKey = 'bbc59887856573ba729af5fe91ac606a';

    function fetchWeatherByCoords(lat, lon) {
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&APPID=${apiKey}&units=metric&lang=kr`;
        fetch(url)
            .then(response => response.json())
            .then(data => updateWeatherWidget(data))
            .catch(error => console.error('Error fetching weather by coords:', error));
    }

    function fetchWeatherByCity(city) {
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&APPID=${apiKey}&units=metric&lang=kr`;
        fetch(url)
            .then(response => response.json())
            .then(data => updateCityCard(city, data))
            .catch(error => console.error(`Error fetching weather for ${city}:`, error));
    }

    function updateWeatherWidget(data) {
        const widget = document.getElementById('weather-widget');
        if (!widget) return;

        if (data.cod === 200) {
            const temp = `${Math.round(data.main.temp)}°C`;
            const description = data.weather[0].description;
            const iconCode = data.weather[0].icon;
            const iconClass = weatherIconMap[iconCode] || 'bi-question-circle';
            const city = data.name;

            widget.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="bi ${iconClass}" style="font-size: 2rem; margin-right: 10px; color: white;"></i>
                    <div>
                        <strong>${city}</strong>
                        <div>${temp}, ${description}</div>
                    </div>
                </div>
            `;
        } else {
            widget.textContent = `오류: ${data.message || '날씨 정보를 가져올 수 없습니다.'}`;
        }
    }

    function updateCityCard(city, data) {
        const card = document.querySelector(`.weather-card[data-city="${city}"]`);
        if (!card) return;

        const cityEl = document.getElementById(`city-${city}`);
        const tempEl = document.getElementById(`temp-${city}`);
        const descEl = document.getElementById(`desc-${city}`);
        const maxTempEl = document.getElementById(`max-temp-${city}`);
        const minTempEl = document.getElementById(`min-temp-${city}`);

        if (data.cod === 200) {
            tempEl.textContent = `${Math.round(data.main.temp)}°`;
            descEl.textContent = data.weather[0].description;
            maxTempEl.textContent = `최고: ${Math.round(data.main.temp_max)}°`;
            minTempEl.textContent = `최저: ${Math.round(data.main.temp_min)}°`;
        } else {
            descEl.textContent = `오류: ${data.message || '정보 없음'}`;
        }
    }

    // --- Main Logic ---
    const weatherWidget = document.getElementById('weather-widget');
    const weatherPage = document.getElementById('weather-page-container');

    if (weatherWidget && typeof weatherCities !== 'undefined') {
        // New logic for the main page widget (random 5 cities)
        const randomCities = weatherCities.sort(() => 0.5 - Math.random()).slice(0, 5);
        
        weatherWidget.innerHTML = ''; // Clear "Loading..." text

        randomCities.forEach(cityPair => {
            const cityEn = cityPair[0];
            const cityKo = cityPair[1];
            const url = `https://api.openweathermap.org/data/2.5/weather?q=${cityEn}&APPID=${apiKey}&units=metric&lang=kr`;
            
            const listItem = document.createElement('div');
            listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            listItem.innerHTML = `<span>${cityKo}</span><span>--°</span>`;
            weatherWidget.appendChild(listItem);

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.cod === 200) {
                        listItem.innerHTML = `
                            <span>${cityKo}</span>
                            <span class="fw-bold">${Math.round(data.main.temp)}°</span>
                        `;
                    } else {
                        listItem.innerHTML = `
                            <span>${cityKo}</span>
                            <span>정보 없음</span>
                        `;
                    }
                })
                .catch(error => {
                    console.error(`Error fetching weather for ${cityEn}:`, error);
                    listItem.innerHTML = `
                        <span>${cityKo}</span>
                        <span>오류</span>
                    `;
                });
        });

    } else if (weatherPage) { // Logic for the dedicated weather page
        const weatherCards = document.querySelectorAll('.weather-card');
        weatherCards.forEach(card => {
            const city = card.dataset.city;
            if (city) {
                fetchWeatherByCity(city);
            }
        });
    }
    
    function fetchWeatherByCityForWidget(city) {
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&APPID=${apiKey}&units=metric&lang=kr`;
        fetch(url)
            .then(response => response.json())
            .then(data => updateWeatherWidget(data))
            .catch(error => console.error(`Error fetching weather for ${city}:`, error));
    }
});