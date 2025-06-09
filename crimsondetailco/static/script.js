// script.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("appointmentForm");
  const confirmation = document.getElementById("confirmation");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const vehicle = document.getElementById("vehicle").value.trim();
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;

    if (!name || !phone || !vehicle || !date || !time) {
      alert("Please fill out all fields before submitting.");
      return;
    }

    // You can expand this to send the form data to a backend later
    confirmation.textContent = `Thank you, ${name}. Your appointment for ${vehicle} on ${date} at ${time} has been submitted.`;
    form.reset();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Auto-format phone input
  const phoneInput = document.getElementById("phone");
  phoneInput.addEventListener("input", function (e) {
    let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    e.target.value = !x[2] ? x[1] : `(${x[1]}) ${x[2]}${x[3] ? '-' + x[3] : ''}`;
  });
});
