document.addEventListener("DOMContentLoaded", function () {
  let signupModal = new bootstrap.Modal(document.getElementById("signupmodal"));
  let loginModal = new bootstrap.Modal(document.getElementById("loginmodal"));

  // Signup Form Submission (AJAX)
  let signupForm = document.getElementById("signup-form");
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
          let errorBox = document.querySelector("#signupmodal .alert-danger");
          errorBox.innerHTML = Object.values(data.error).join("<br>");
          errorBox.style.display = "block";
        }
      });
  });
}
  // Login Form Submission (AJAX)
let loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
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
          let errorBox = document.querySelector("#loginmodal .alert-danger");
          errorBox.innerHTML = data.error; // Login returns a single error message
          errorBox.style.display = "block";
        }
      });
  });
}
  // Switch between modals
  let switchToLogin = document.querySelector(".switch-to-login");
if (switchToLogin) {
  switchToLogin.addEventListener("click", function () {
    signupModal.hide();
    setTimeout(() => loginModal.show(), 500);
  });
}

let switchToRegister = document.querySelector(".switch-to-register");
if (switchToRegister) {
  switchToRegister.addEventListener("click", function () {
    loginModal.hide();
    setTimeout(() => signupModal.show(), 500);
  });
}

  // Close modals when clicking "X" or close buttons
  document.querySelectorAll(".close-modal").forEach((btn) => {
    btn.addEventListener("click", function () {
      signupModal.hide();
      loginModal.hide();
    });
  });
});






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



// document.addEventListener("DOMContentLoaded", function () {
//     let signupModal = new bootstrap.Modal(document.getElementById("signupmodal"));
//     let loginModal =  new bootstrap.Modal(document.getElementById("loginmodal"));
//     // Check if there are form errors on page load (after a failed submission)
//     if (document.querySelector("#loginModal .alert-danger")) {
//       loginModal.show();
//     }
  
//     // Keep Signup Modal open if there's a signup error
//     if (document.querySelector("#signupModal .alert-danger")) {
//       signupModal.show();
//     }
//     document.querySelector(".switch-to-login").addEventListener("click",function(){
//       signupModal.hide();
//       setTimeout(() => loginModal.show(),500);
//     })
//     document.querySelector(".switch-to-register").addEventListener("click",function(){
//       loginModal.hide();
//       setTimeout(() => signupModal.show(),500);
//     })
//     // Ensure the modal can still be closed manually
//     document.querySelectorAll(".close-modal").forEach((btn) => {
//       btn.addEventListener("click", function () {
//         signupModal.hide();
//         loginModal.hide();
//       });
//     });
//   });
  

