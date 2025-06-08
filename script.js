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

    fetch("/api/book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name, phone, vehicle, date, time })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        confirmation.textContent = `✅ Thank you, ${name}. Your appointment for ${vehicle} on ${date} at ${time} has been booked!`;
        confirmation.style.display = "block";
        form.reset();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => confirmation.style.display = "none", 8000);
      } else {
        alert(`❌ ${data.message}`);
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Something went wrong while booking your appointment.");
    });
  });

  const phoneInput = document.getElementById("phone");
  phoneInput.addEventListener("input", function (e) {
    let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    e.target.value = !x[2] ? x[1] : `(${x[1]}) ${x[2]}${x[3] ? '-' + x[3] : ''}`;
  });
});
