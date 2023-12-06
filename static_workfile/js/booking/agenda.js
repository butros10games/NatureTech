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
    } else if (!endDate || (startDate && Math.abs(newDate - endDate) < Math.abs(newDate - startDate))) {
        endDate = newDate;
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
