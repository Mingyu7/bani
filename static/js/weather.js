document.addEventListener('DOMContentLoaded', function() {
    const apiKey = 'YOUR_API_KEY'; // IMPORTANT: Replace with your OpenWeatherMap API key
    const city = 'Seoul';
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    const cityEl = document.getElementById('city');
    const tempEl = document.getElementById('temp');
    const weatherDescEl = document.getElementById('weather-desc');

    if (apiKey === 'YOUR_API_KEY') {
        cityEl.textContent = 'API Key Needed';
        weatherDescEl.textContent = 'Please add your OpenWeatherMap API key in static/js/weather.js';
        return;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.cod === 200) {
                cityEl.textContent = data.name;
                tempEl.textContent = `${data.main.temp} °C`;
                weatherDescEl.textContent = data.weather[0].description;
            } else {
                cityEl.textContent = 'Error';
                weatherDescEl.textContent = data.message;
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            cityEl.textContent = 'Error';
            weatherDescEl.textContent = 'Could not fetch weather data.';
        });
});