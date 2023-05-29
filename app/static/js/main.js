const darkModeToggle = document.querySelector('#dark-mode-toggle');
const body = document.querySelector('body');

darkModeToggle.addEventListener('change', () => {
  if (darkModeToggle.checked) {
    body.classList.add('dark-mode');
    body.classList.remove('light-mode');
  } else {
    body.classList.add('light-mode');
    body.classList.remove('dark-mode');
  }
});



const profileArrow = document.querySelector('.profile-arrow');

profileArrow.addEventListener('click', () => {
  profileArrow.classList.toggle('rotate');
  // Add code to show/hide menu here
  const profileMenu = document.querySelector('.profile-menu');
  profileMenu.classList.toggle('show-menu');
});




document.addEventListener("DOMContentLoaded", function() {
  const loginForm = document.getElementById("loginForm");
  const registrationFormContainer = document.getElementById("registrationFormContainer");

  const toggleRegistration = document.getElementById("toggleRegistration");
  const toggleLogin = document.getElementById("toggleLogin");

  toggleRegistration.addEventListener("click", function(event) {
    event.preventDefault();
    loginForm.style.display = "none";
    registrationFormContainer.style.display = "block";
  });

  toggleLogin.addEventListener("click", function(event) {
    event.preventDefault();
    loginForm.style.display = "block";
    registrationFormContainer.style.display = "none";
  });
});

