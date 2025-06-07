document.getElementById("booking-form").addEventListener("submit", async function(e) {
  e.preventDefault();

  const response = await fetch("/api/book", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("name").value,
      phone: document.getElementById("phone").value,
      vehicle: document.getElementById("vehicle").value,
      date: document.getElementById("date").value,
      time: document.getElementById("time").value
    })
  });

  const data = await response.json();
  const msg = document.getElementById("message");
  msg.textContent = data.message;
  msg.style.color = data.success ? "green" : "red";
});