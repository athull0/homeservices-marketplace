document.addEventListener("DOMContentLoaded", function () {
  let authModal = new bootstrap.Modal(document.getElementById('authmodal'));
  let signupForm = document.getElementById("signupform");
  let loginForm  = document.getElementById('loginform');
  let modalTitle = document.getElementById("modaltitle")
  let loginErrorDiv = document.getElementById("login-error")
  let signupErrorDiv = document.getElementById("signup-error");
  
  
    if (sessionStorage.getItem("loggedIn") === "true") {
      sessionStorage.removeItem("loggedIn"); // Reset flag
      return; // Stop further execution
    }
    if (sessionStorage.getItem("signedUp") === "true") {
      sessionStorage.removeItem("signedUp"); // Reset flag
      return;
    }
    
  document.getElementById("login-form").addEventListener("submit", function (event) {
      event.preventDefault(); 
    let formData = new FormData(this);
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(loginUrl, {
        method: "POST",
        body: formData,
        
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
          authModal.hide();
          sessionStorage.setItem("loggedIn", "true");
          setTimeout(() => location.reload(), 500);
            
              // Refresh the page after successful login
        } else {
            
          loginErrorDiv.style.display = "block";
          loginErrorDiv.textContent = data.error;
          authModal.show();

        }
    })
    .catch(error => console.error("Error:", error));
});
if (document.querySelector("#signupform .alert-danger")) {
  authModal.show();
}
document.getElementById("signup-form").addEventListener("submit", function (event) {
  event.preventDefault();
  let formData = new FormData(this);
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch(registerUrl, {

    method: "POST",
    body: formData,
    headers:{
      "x-CSRFToken": csrfToken
    }
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        authModal.hide();
        sessionStorage.setItem("signedUp", "true"); // Store signup status
        setTimeout(() => location.reload(), 500);
      } else {
        signupErrorDiv.style.display = "block";
        signupErrorDiv.textContent = data.error;
      }
    })
    .catch((error) => console.error("Error:", error));
});

    // Check if there are form errors on page load (after a failed submission)
//     if (document.querySelector("#signupform .alert-danger") || 
//     document.querySelector("#loginform .alert-danger")) {
//     authModal.show();
// }

    document.querySelector(".switch-to-login").addEventListener("click",function(){
      signupForm.style.display = "none";
      loginForm.style.display = "block";
      modalTItle.textContent = "Login";
    })
    document.querySelector(".switch-to-register").addEventListener("click",function(){
      loginForm.style.display = "none";
      signupForm.style.display = "block";
      modalTitle.textContent = "Register";
    })
    // Ensure the modal can still be closed manually
  //   document.querySelectorAll("form").forEach(form => {
  //     form.addEventListener("submit", function (event) {
  //         setTimeout(() => {
  //             let errorAlert = form.querySelector(".alert-danger");
  //             if (errorAlert && errorAlert.innerHTML.trim() !== "") {
  //                 authModal.show();  // Keep modal open if errors exist
  //             }
  //         }, 100);  // Delay checking errors slightly to let Django reload them
  //     });
  // });
  
  
    document.querySelectorAll(".close-modal").forEach((btn) => {
      btn.addEventListener("click", function () {
        authModal.hide();
        
      });
    });
  });
  
  
