function sendMessage() {
    const message = document.getElementById("messageInput").value;
    fetch("{% url 'send_message' %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}"
      },
      body: JSON.stringify({
        message: message,
        receiver_id: "{{ receiver.id }}"
      })
    })
    .then(response => response.json())
    .then(data => {
      const chatBox = document.getElementById("chat-box");
      chatBox.innerHTML += `<p><strong>${data.sender}:</strong> ${data.message}</p>`;
      document.getElementById("messageInput").value = "";
      chatBox.scrollTop = chatBox.scrollHeight;
    });
  }