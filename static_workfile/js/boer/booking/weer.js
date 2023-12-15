function renderWeather(weather) {
    console.log(weather);
    var result = document.getElementById("weer");

    renderDay(result, weather.list[0], weather.list[0].dt_txt);
    renderDay(result, weather.list[8], weather.list[8].dt_txt);
    renderDay(result, weather.list[16], weather.list[16].dt_txt);
    renderDay(result, weather.list[24], weather.list[24].dt_txt);
    renderDay(result, weather.list[32], weather.list[32].dt_txt);
}

function renderDay(result, dayData, dateString) {
    // Format the date
    const formattedDate = formatDateString(dateString);

    var dateElement = document.createElement("p");
    dateElement.classList.add("date");
    dateElement.textContent = formattedDate;
    result.appendChild(dateElement);

    var temp = document.createElement("p");
    temp.classList.add("temp");
    temp.textContent = "Temperatuur " + ": " + dayData.main.temp + "°C";
    result.appendChild(temp);

    var feelsLike = document.createElement("p");
    feelsLike.classList.add("feelsLike");
    feelsLike.textContent = "Gevoel: " + dayData.main.feels_like + "°C";
    result.appendChild(feelsLike);

    var humidity = document.createElement("p");
    humidity.classList.add("humidity");
    humidity.textContent = "Luchtvochtigheid: " + dayData.main.humidity + "%";
    result.appendChild(humidity);

    var wind = document.createElement("p");
    wind.classList.add("wind");
    wind.textContent = "Wind: " + dayData.wind.speed + "km/h";
    result.appendChild(wind);

    var iconCode = dayData.weather[0].icon;
    var iconUrl = "https://openweathermap.org/img/wn/" + iconCode + ".png";
    var icon = document.createElement("img");
    icon.classList.add("icon");
    icon.src = iconUrl;
    icon.alt = "Weather Icon";
    result.appendChild(icon);
}

function formatDateString(dateString) {
    // Parse the input date string
    const date = new Date(dateString);

    // Get day and month components
    const day = date.getDate();
    const month = date.getMonth() + 1; // Months are zero-based, so add 1

    // Pad single-digit day and month with leading zero if needed
    const formattedDay = day < 10 ? '0' + day : day;
    const formattedMonth = month < 10 ? '0' + month : month;

    // Create the formatted date string in the "DD-MM" format
    const formattedDateString = `${formattedDay}-${formattedMonth}`;

    return formattedDateString;
}

function fetchWeather(){
var url = "https://api.openweathermap.org/data/2.5/forecast?lat=52.122860&lon=5.151870&appid=ecb2c229c444da2509af110aae3d4dbf&units=metric";

fetch(url)
    .then((response) => response.json())
    .then((data) => renderWeather(data))
    .catch((error) => console.error("Error fetching weather:", error));
}

fetchWeather();
