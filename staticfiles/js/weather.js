document.addEventListener('DOMContentLoaded', function() {
    const apiKey = 'bbc59887856573ba729af5fe91ac606a';
    // Map OpenWeatherMap icons to Bootstrap Icons
    const weatherIconMap = {
        '01d': 'bi-sun', '01n': 'bi-moon',
        '02d': 'bi-cloud-sun', '02n': 'bi-cloud-moon',
        '03d': 'bi-cloud', '03n': 'bi-cloud',
        '04d': 'bi-cloud-fill', '04n': 'bi-cloud-fill',
        '09d': 'bi-cloud-rain', '09n': 'bi-cloud-rain',
        '10d': 'bi-cloud-drizzle', '10n': 'bi-cloud-drizzle',
        '11d': 'bi-cloud-lightning', '11n': 'bi-cloud-lightning',
        '13d': 'bi-cloud-snow', '13n': 'bi-cloud-snow',
        '50d': 'bi-cloud-fog', '50n': 'bi-cloud-fog'
    };

    // Function to update the main weather widget (for Cheonan)
    function updateCheonanWeatherWidget(data) {
        const widget = document.getElementById('weather-widget');
        if (!widget) return;

        if (data.cod === 200) {
            const temp = Math.round(data.main.temp);
            const description = data.weather[0].description;
            const iconCode = data.weather[0].icon;
            const iconClass = weatherIconMap[iconCode] || 'bi-question-circle';
            const maxTemp = Math.round(data.main.temp_max);
            const minTemp = Math.round(data.main.temp_min);

            widget.innerHTML = `
                <div class="weather-main-card">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0">${data.name}</h6>
                        <i class="bi ${iconClass}" style="font-size: 2rem;"></i>
                    </div>
                    <div class="current-temp">${temp}°</div>
                    <div class="description mb-2">${description}</div>
                    <div class="temp-range">최고: ${maxTemp}° 최저: ${minTemp}°</div>
                </div>
                <div id="other-cities-weather" class="list-group list-group-flush mt-3"></div>
            `;
        } else {
            widget.innerHTML = `<div class="weather-main-card">오류: ${data.message || '날씨 정보를 가져올 수 없습니다.'}</div>`;
        }
    }

    // Function to update other city weather (simple list item)
    function updateOtherCityWeather(cityKo, data) {
        const otherCitiesWidget = document.getElementById('other-cities-weather');
        if (!otherCitiesWidget) return;

        const listItem = document.createElement('div');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        
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
        otherCitiesWidget.appendChild(listItem);
    }

    // --- Main Logic ---
    const weatherWidget = document.getElementById('weather-widget');
    const weatherPage = document.getElementById('weather-page-container');

    if (weatherWidget && typeof weatherCities !== 'undefined') {
        weatherWidget.innerHTML = '<div class="list-group-item">로딩 중...</div>'; // Show loading initially

        const cheonanEn = weatherCities[0][0];
        const cheonanKo = weatherCities[0][1];

        // Fetch Cheonan weather first and display in detail
        const cheonanUrl = `https://api.openweathermap.org/data/2.5/weather?q=${cheonanEn}&APPID=${apiKey}&units=metric&lang=kr`;
        fetch(cheonanUrl)
            .then(response => response.json())
            .then(data => updateCheonanWeatherWidget(data))
            .catch(error => console.error(`Error fetching weather for ${cheonanEn}:`, error));

        // Fetch and display other cities
        for (let i = 1; i < weatherCities.length; i++) {
            const cityPair = weatherCities[i];
            const cityEn = cityPair[0];
            const cityKo = cityPair[1];
            const url = `https://api.openweathermap.org/data/2.5/weather?q=${cityEn}&APPID=${apiKey}&units=metric&lang=kr`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => updateOtherCityWeather(cityKo, data))
                .catch(error => console.error(`Error fetching weather for ${cityEn}:`, error));
        }

    } else if (weatherPage) { // Logic for the dedicated weather page
        const weatherCards = document.querySelectorAll('.weather-card');
        weatherCards.forEach(card => {
            const city = card.dataset.city;
            if (city) {
                fetchWeatherByCity(city);
            }
        });
    }
    
    // Keep existing functions for weather page if they are used
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
        // This function is now only used by fetchWeatherByCoords, if at all
        // Its logic is largely replaced by updateCheonanWeatherWidget for the main widget
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
});