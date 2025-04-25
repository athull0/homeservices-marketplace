document.addEventListener("DOMContentLoaded", function () {
    let wsignupModal = new bootstrap.Modal(document.getElementById("workersignupmodal"));
    let wloginModal = new bootstrap.Modal(document.getElementById("workerloginmodal"));
  
    // Signup Form Submission (AJAX)
    let signupForm = document.getElementById("wsignup-form");
    if (signupForm) {
      signupForm.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent page reload
        let formData = new FormData(this);
    
  
      fetch(this.action, {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            location.reload(); // Reload the page on success
          } else {
            let errorBox = document.querySelector("#workersignupmodal .alert-danger");
            errorBox.innerHTML = Object.values(data.error).join("<br>");
            errorBox.style.display = "block";
          }
        });
    });
  }
    // Login Form Submission (AJAX)
  let wloginForm = document.getElementById("wlogin-form");
  if (wloginForm) {
    wloginForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent page reload
      let formData = new FormData(this);
  
  
      fetch(this.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,  // Get CSRF token from form
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.href = "/home/"; // Reload the page on successful login
          } else {
            let errorBox = document.querySelector("#workerloginmodal .alert-danger");
            errorBox.innerHTML = data.error; // Login returns a single error message
            errorBox.style.display = "block";
          }
        });
    });
  }
    // Switch between modals
    let switchToLogin = document.querySelector(".switch-to-worker-login");
  if (switchToLogin) {
    switchToLogin.addEventListener("click", function () {
      wsignupModal.hide();
      setTimeout(() => wloginModal.show(), 500);
    });
  }
  
  let switchToRegister = document.querySelector(".switch-to-worker-register");
  if (switchToRegister) {
    switchToRegister.addEventListener("click", function () {
      wloginModal.hide();
      setTimeout(() => wsignupModal.show(), 500);
    });
  }
  
    // Close modals when clicking "X" or close buttons
    document.querySelectorAll(".close-modal").forEach((btn) => {
      btn.addEventListener("click", function () {
        wsignupModal.hide();
        wloginModal.hide();
      });
    });
  });
  