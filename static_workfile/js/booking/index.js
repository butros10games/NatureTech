const slide_button = document.getElementById('slide-button');
const fake_container = document.getElementById('fake-container');
const map_container = document.getElementById('map-container');
const form_container = document.getElementById('form-container');

slide_button.addEventListener('click', () => {
    map_container.classList.toggle('expanded');
    
    if (map_container.classList.contains('expanded')) {
        form_container.style.transform = 'translateX(100%)';
        slide_button.style.transform = 'rotate(180deg)';
    } else {
        form_container.style.transform = 'translateX(0)';
        slide_button.style.transform = 'rotate(0deg)';
    }
});
