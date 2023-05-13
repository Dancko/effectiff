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
