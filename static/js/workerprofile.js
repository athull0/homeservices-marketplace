document.getElementById("availability-checkbox").addEventListener("change", function() {
    fetch("{% url 'toggle_availability' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Availability updated:", data.availability);
    })
    .catch(error => console.error("Error:", error));
});