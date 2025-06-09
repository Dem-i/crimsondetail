// Toggle dropdown menu
function toggleMenu() {
  const menu = document.getElementById("menu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

// DOM logic for form validation and interaction
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const dateInput = document.querySelector('input[name="date"]');
  const phoneInput = document.querySelector('input[name="phone"]');
  const emailInput = document.querySelector('input[name="email"]');
  const nameInput = document.querySelector('input[name="name"]');
  const serviceInput = document.querySelector('input[name="service"]');
  const timeInput = document.querySelector('input[name="time"]');
  const confirmation = document.createElement("div");
  confirmation.id = "confirmation";
  confirmation.style.textAlign = "center";
  confirmation.style.color = "#ffd700";
  form.parentNode.insertBefore(confirmation, form);

  // Prevent weekend bookings
  dateInput.addEventListener("change", function () {
    const day = new Date(this.value).getDay();
    if (day === 6 || day === 0) {
      alert("Bookings are not allowed on Saturdays and Sundays.");
      this.value = "";
    }
  });

  // Validate phone or email on submit
  form.addEventListener("submit", function (e) {
    if (!nameInput.value.trim() || !serviceInput.value.trim() || !timeInput.value || !dateInput.value) {
      e.preventDefault();
      alert("Please fill out all required fields.");
      return;
    }
    if (!phoneInput.value.trim() && !emailInput.value.trim()) {
      e.preventDefault();
      alert("Please provide at least a phone number or an email address.");
      return;
    }

    // Confirmation message (client-side)
    e.preventDefault();
    confirmation.textContent = `Thank you, ${nameInput.value.trim()}. Your appointment for ${serviceInput.value.trim()} on ${dateInput.value} at ${timeInput.value} has been submitted.`;
    form.reset();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Auto-format phone number
  phoneInput.addEventListener("input", function (e) {
    let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    e.target.value = !x[2] ? x[1] : `(${x[1]}) ${x[2]}${x[3] ? '-' + x[3] : ''}`;
  });
});
