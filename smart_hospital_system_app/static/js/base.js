const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

menuToggle.addEventListener("click", function () {
  navMenu.classList.toggle("active");
});

const navLinks = navMenu.querySelectorAll("a");

navLinks.forEach((link) => {
  link.addEventListener("click", function () {
    navMenu.classList.remove("active");
  });
});

document.addEventListener("click", function (e) {
  if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
    navMenu.classList.remove("active");
  }
});
