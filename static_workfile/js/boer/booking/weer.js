function renderWeather(weather) {
    console.log(weather);
    var result = document.getElementById("weer");

    var temp = document.createElement("p");
    temp.textContent = "Temp: " + weather.main.temp + "°C";
    result.appendChild(temp);

    var humidity = document.createElement("p");
    humidity.textContent = "Humidity: " + weather.main.humidity + "%";
    result.append(humidity);

    var wind = document.createElement("p");
    wind.textContent = "wind: " + weather.wind.speed + "km/h"
    result.append(wind);

    details.append("")
}

function fetchWeather(query) {
    var url =
        "https://api.openweathermap.org/data/2.5/weather?lat=52.122860&lon=5.151870&appid=ecb2c229c444da2509af110aae3d4dbf&units=metric";


    fetch(url)
        .then((response) => response.json())
        .then((data) => renderWeather(data))
}

fetchWeather()