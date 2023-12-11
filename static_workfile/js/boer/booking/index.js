const slide_button = document.getElementById('slide-button');
const fake_container = document.getElementById('fake-container');
const map_container = document.getElementById('map-container');
const form_container = document.getElementById('form-container');

slide_button.addEventListener('click', () => {
    map_container.classList.toggle('expanded');
    
    if (map_container.classList.contains('expanded')) {
        form_container.style.transform = 'translateX(calc(100% + 18px))';
        slide_button.style.transform = 'rotate(180deg)';

        // click on all the dropdowns to close them
        setTimeout(() => {
            document.querySelectorAll('#toggleButton').forEach(dropdown => {
                rotateButtonCheck = dropdown.querySelector('#rotateButton');

                // check if the dropdown is open
                if (!rotateButtonCheck.classList.contains('closed')) {
                    // if so, close it
                    dropdown.click();
                }
            });
        }, 50);
    } else {
        form_container.style.transform = 'translateX(0)';
        slide_button.style.transform = 'rotate(0deg)';

        document.querySelectorAll('#toggleButton').forEach(dropdown => {
            dropdown.click();
        });
    }
});
