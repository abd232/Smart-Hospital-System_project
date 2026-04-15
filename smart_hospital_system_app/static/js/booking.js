const timeSlotsContainer = document.getElementById("timeSlots");
const bookingForm = document.getElementById("bookingForm");
const selectedTimeInput = document.getElementById("selectedTimeInput");

const timeSlots = [
  "09:00 AM",
  "10:00 AM",
  "11:00 AM",
  "01:00 PM",
  "02:00 PM",
  "03:00 PM",
];

let selectedTime = null;

// Generate time slots dynamically
timeSlots.forEach((slot) => {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = slot;
  button.className =
    "time-slot p-3 border rounded-xl text-gray-700 hover:bg-blue-100";

  button.addEventListener("click", () => {
    selectedTime = slot;
    selectedTimeInput.value = slot;

    document
      .querySelectorAll(".time-slot")
      .forEach((b) => b.classList.remove("selected"));

    button.classList.add("selected");
  });

  timeSlotsContainer.appendChild(button);
});

// Handle form submission
bookingForm.addEventListener("submit", (e) => {
  const date = document.getElementById("date").value;

  if (!date) {
    e.preventDefault();
    alert("Please select a date!");
    return;
  }

  if (!selectedTime) {
    e.preventDefault();
    alert("Please select a time slot!");
    return;
  }
});
