function renderWeather(weather) {
    console.log(weather);
    var result = document.getElementById("weer");

    var temp = document.createElement("p");
    temp.classList.add("temp");
    temp.textContent = "Temperatuur: " + weather.main.temp + "°C";
    result.appendChild(temp);

    var humidity = document.createElement("p");
    humidity.classList.add("humidity");
    humidity.textContent = "Luchtvochtigheid: " + weather.main.humidity + "%";
    result.appendChild(humidity);

    var wind = document.createElement("p");
    wind.classList.add("wind");
    wind.textContent = "Wind: " + weather.wind.speed + "km/h";
    result.appendChild(wind);

    var feelsLike = document.createElement("p");
    feelsLike.classList.add("feelsLike");
    feelsLike.textContent = "Gevoel: " + weather.main.feels_like + "°C";
    result.appendChild(feelsLike);

    var iconCode = weather.weather[0].icon;
    var iconUrl = "https://openweathermap.org/img/wn/" + iconCode + ".png";
    var icon = document.createElement("img");
    icon.classList.add("icon");
    icon.src = iconUrl;
    icon.alt = "Weather Icon";
    result.appendChild(icon);
}

function fetchWeather() {
    var url = "https://api.openweathermap.org/data/2.5/weather?lat=52.122860&lon=5.151870&appid=ecb2c229c444da2509af110aae3d4dbf&units=metric";

    fetch(url)
        .then((response) => response.json())
        .then((data) => renderWeather(data))
}

fetchWeather();
