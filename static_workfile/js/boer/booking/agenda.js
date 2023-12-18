const daysTag = document.querySelector(".days"),
      currentDate = document.querySelector(".current-date"),
      prevNextIcon = document.querySelectorAll(".icons span");

let date = new Date(),
    currYear = date.getFullYear(),
    currMonth = date.getMonth(),
    currDay = date.getDate();

let startDate = null, endDate = null;

const months = ["January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"];

const renderCalendar = () => {
    let firstDayOfMonth = new Date(currYear, currMonth, 1).getDay(),
        lastDateOfMonth = new Date(currYear, currMonth + 1, 0).getDate(),
        lastDayOfMonth = new Date(currYear, currMonth, lastDateOfMonth).getDay(),
        lastDateOfLastMonth = new Date(currYear, currMonth, 0).getDate();

    let liTag = "";

    for (let i = firstDayOfMonth; i > 0; i--) {
        let today = new Date();
        today.setHours(0, 0, 0, 0);
        let currentDate = new Date(currYear, currMonth, i);
        let isPast = currentDate < today;
        liTag += `<li class="inactive ${isPast ? 'past' : ''}" data-day="${lastDateOfLastMonth - i + 1}" data-month="${currMonth - 1}" data-year="${currYear}">${lastDateOfLastMonth - i + 1}</li>`;
    }

    for (let i = 1; i <= lastDateOfMonth; i++) {
        let today = new Date();
        today.setHours(0, 0, 0, 0);
        let currentDate = new Date(currYear, currMonth, i);
        let isPast = currentDate < today;
        liTag += `<li ${isPast ? 'class="past"' : ''} data-day="${i}" data-month="${currMonth}" data-year="${currYear}">${i}</li>`;
    }

    for (let i = lastDayOfMonth; i < 6; i++) {
        let today = new Date();
        today.setHours(0, 0, 0, 0);
        let currentDate = new Date(currYear, currMonth + 1, i);
        let isPast = currentDate < today;
        liTag += `<li class="inactive ${isPast ? 'past' : ''}" data-day="${i - lastDayOfMonth + 1}" data-month="${currMonth + 1}" data-year="${currYear}">${i - lastDayOfMonth + 1}</li>`;
    }

    currentDate.innerText = `${months[currMonth]} ${currYear}`;
    daysTag.innerHTML = liTag;

    highlightSelection();
    addDayCellEventListeners();
    setPsudoElement();
};

const updateDateSelection = (selectedYear, selectedMonth, selectedDay) => {
    let newDate = new Date(selectedYear, selectedMonth, selectedDay);
    if (startDate && +startDate === +newDate || endDate && +endDate === +newDate) {
        startDate = null;
        endDate = null;
    } else if (!startDate || (endDate && Math.abs(newDate - startDate) < Math.abs(newDate - endDate))) {
        startDate = newDate;

        if (endDate != null && startDate != null) {
            availability_request()
        }
        
    } else if (!endDate || (startDate && Math.abs(newDate - endDate) < Math.abs(newDate - startDate))) {
        endDate = newDate;

        availability_request()
    } else {
        startDate = newDate;
        endDate = null;
    }

    if (startDate && endDate && startDate > endDate) {
        let temp = startDate;
        startDate = endDate;
        endDate = temp;
    }
    highlightSelection();
};

const highlightSelection = () => {
    document.querySelectorAll('.days li').forEach(li => {
        li.classList.remove('selected', 'range', 'first', 'last', 'halfLine');
        let day = parseInt(li.getAttribute("data-day"));
        let month = parseInt(li.getAttribute("data-month"));
        let year = parseInt(li.getAttribute("data-year"));
        let liDate = new Date(year, month, day);

        if ((startDate && liDate.getTime() === startDate.getTime()) ||
            (endDate && liDate.getTime() === endDate.getTime())) {
            li.classList.add('selected');

            // Add to the first day of the range the class 'first'
            if (startDate && liDate.getTime() === startDate.getTime()) {
                li.classList.add('first');
            }

            // Add to the last day of the range the class 'last'
            if (endDate && liDate.getTime() === endDate.getTime()) {
                li.classList.add('last');
            }

            // when there are two days selected add the class `halfLine` to the two selected days
            if (startDate && endDate) {
                li.classList.add('halfLine');
            } else if (startDate && !endDate) {
                // when there is only one day selected, remove the `halfLine` class from all selected elements
                document.querySelectorAll('.halfLine').forEach(el => el.classList.remove('halfLine'));
            }
        }

        if (startDate && endDate && liDate > startDate && liDate < endDate) {
            li.classList.add('range');
        }
    });
};

const addDayCellEventListeners = () => {
    document.querySelectorAll(".days li").forEach((day) => {
        day.addEventListener("click", () => {
            const selectedDay = parseInt(day.getAttribute("data-day"));
            const selectedMonth = parseInt(day.getAttribute("data-month"));
            const selectedYear = parseInt(day.getAttribute("data-year"));

            let today = new Date();
            today.setHours(0, 0, 0, 0);
            let selectedDate = new Date(selectedYear, selectedMonth, selectedDay);

            if (selectedDate >= today) {
                updateDateSelection(selectedYear, selectedMonth, selectedDay);
            }
        });
    });
};

prevNextIcon.forEach(icon => {
    icon.addEventListener("click", () => {
        currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;

        if (currMonth < 0) {
            currMonth = 11;
            currYear--;
        } else if (currMonth > 11) {
            currMonth = 0;
            currYear++;
        }
        renderCalendar();
    });
});

renderCalendar();

function plekSelectionUpdate(available_places) {
    const plekSelectieContainer = document.getElementById('plekSelectieContainer');

    plekSelectieContainer.innerHTML = '';

    available_places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.className = 'w-full sm:w-1/2 px-2 mb-4';
        placeElement.innerHTML = `
            <div class="flex items-center border p-2 cursor-pointer" onclick="toggleCheckbox('${place.id}')">
                <input type="checkbox" id="${place.id}" name="${place.id}" value="${place.id}" class="mr-2 hidden">
                <span class="checkbox-custom mr-2"></span>
                <div class="flex-grow">
                    <p class="mr-2">${place.name}</p>
                </div>
                <p>€ ${place.price}</p>
            </div>
        `;
        plekSelectieContainer.appendChild(placeElement);
    });
}

function availability_request() {
    // Format the dates to YYYY-MM-DD before sending
    let formattedStartDate = startDate.toISOString().split('T')[0];
    let formattedEndDate = endDate.toISOString().split('T')[0];

    let availability_data = {
        'csrfmiddlewaretoken': document.getElementById('csrfmiddlewaretoken').innerHTML,
        'startDate': formattedStartDate,
        'endDate': formattedEndDate
    };

    $.ajax({
        type: 'POST',
        url: "beschikbaarheidsCheck/",
        data: availability_data,
        success: function (data) {
            console.log(data)
            if (data['status'] == 'success') {
                plekSelectionUpdate(data.available_places)
            } else {
                alert('Er is iets fout gegaan, probeer het later opnieuw.')
            }
        },
        error: function (data) {
            console.log(data)
            if (data.type === 'rate_limit') {
                alert(data.message)
            } else {
                alert('Er is iets fout gegaan, probeer het later opnieuw.')
            }
        }
    });
}