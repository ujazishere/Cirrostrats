// JavaScript code for toggling the burger menu, sidebar, and dark mode
document.addEventListener("DOMContentLoaded", function () {
  var burgerMenu = document.querySelector(".burger-menu");
  var sidebar = document.querySelector(".sidebar");

  burgerMenu.addEventListener("click", function () {
    sidebar.classList.toggle("active");
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var initialMode = localStorage.getItem("selectedMode");
  if (initialMode === "dark") {
    document.body.classList.add("dark-mode");
  }

  // Update the dark mode switch button's content
  updateButtonContent(initialMode === "dark");
});

function toggleDarkMode() {
  var body = document.body;
  body.classList.toggle("dark-mode");
  var isDarkMode = body.classList.contains("dark-mode");

  // Update button content based on the mode
  updateButtonContent(isDarkMode);

  // Save the selected mode to localStorage
  var selectedMode = isDarkMode ? "dark" : "light";
  localStorage.setItem("selectedMode", selectedMode);
}

function updateButtonContent(isDarkMode) {
  var modeButton = document.querySelector(".dark-mode-switch button");

  // Set the initial background image
  modeButton.style.backgroundImage = isDarkMode
    ? 'url("https://www.svgrepo.com/download/381213/dark-mode-night-moon.svg")'
    : 'url("https://www.svgrepo.com/download/433086/light-mode.svg")';

  // Adjust the size of the SVG image
  modeButton.style.backgroundSize = isDarkMode ? "70%" : "26px 26px"; // You can adjust the size as needed
  modeButton.style.backgroundRepeat = "no-repeat";
  modeButton.style.width = "35px"; // Set the width of the button
  modeButton.style.height = "35px"; // Set the height of the button
  modeButton.style.backgroundPosition = "center";
}

// Check and set the mode on page load
document.addEventListener("DOMContentLoaded", function () {
  var selectedMode = localStorage.getItem("selectedMode");
  if (selectedMode === "dark") {
    var body = document.body;
    body.classList.add("dark-mode");
  }
});

// Check and set the mode on page load
document.addEventListener("DOMContentLoaded", function () {
  var selectedMode = localStorage.getItem("selectedMode");
  if (selectedMode === "dark") {
    var body = document.body;
    body.classList.add("dark-mode");
    document.getElementById("darkModeToggle").checked = true;
  }
});

// Function to update the GMT clock with date (without year), hours, and minutes
function updateGMTClock() {
  var gmtTimeElement = document.getElementById("gmt-time");
  var now = new Date();
  var day = now.getUTCDate().toString().padStart(2, "0");
  var month = (now.getUTCMonth() + 1).toString().padStart(2, "0"); // Adding 1 as months are zero-based
  var year = now.getUTCFullYear();
  var hours = now.getUTCHours().toString().padStart(2, "0");
  var minutes = now.getUTCMinutes().toString().padStart(2, "0");
  var gmtTime = day + " " + hours + minutes;
  gmtTimeElement.textContent = "" + gmtTime + "Z";
}

// Update the GMT clock initially and set an interval to update it every second
document.addEventListener("DOMContentLoaded", function () {
  updateGMTClock(); // Update the GMT clock initially
  setInterval(updateGMTClock, 1000); // Update it every second
});

var body = document.getElementsByTagName("body")[0];
var removeLoading = function () {
  setTimeout(function () {
    body.className = body.className.replace(/loading/, "");
  }, 3000);
};
removeLoading();
